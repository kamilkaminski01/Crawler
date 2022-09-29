import requests
import bs4
import fnmatch
import pandas as pd
import mysql.connector
import pymysql
import time

# Połączenie do lokalnej bazy danych MySQL
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="kamil123",
#     database="testdatabase"
# )


# Połączenie do bazy danych MySQL w AWS
db = pymysql.connect(
    host="gov-crawler.ces9mzhykkcv.eu-central-1.rds.amazonaws.com",
    user="admin",
    password="i11ABnAs3KIp7IrwgOhkYQlPF9E3hxH1",
    database="gov-crawler"
)
cursor = db.cursor()


url_nr_posiedzenia = '*agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=*'
url_home_link = 'https://www.sejm.gov.pl/Sejm9.nsf/'
url_home_link2 = 'https://www.sejm.gov.pl'
url_glosowania_partii = '*agent.xsp?symbol=klubglos&IdGlosowania=*'
url_posiedzen = 'https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=posglos&NrKadencji=9'
url_glosowan = 'https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=listaglos&IdDnia='
url_poslowie = 'https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=C'
url_posla = '*posel.xsp?id=*'
url_glos_posla = 'https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=POSELGL&NrKadencji=9&Nrl='


# Funkcja do wypełnienia listy id_posiedzen
def get_id_posiedzen_list():
    id_posiedzen_list = []

    # Wczytanie strony ze zmiennej url_posiedzen
    soup = bs4.BeautifulSoup(requests.get(url_posiedzen, verify=True).text, 'html.parser')

    # Wyszukiwanie linków dat posiedzeń i pobranie od nich ID
    for link in soup.find_all('a'):
        link = link.get('href')
        if fnmatch.fnmatch(link, '*IdDnia=*'):
            link = link[link.index('IdDnia='):].strip('IdDnia=')
            id_posiedzen_list.append(link)

    return id_posiedzen_list


# Funkcja do wypełnienia listy id_posłów
def get_id_poslow_list():
    id_poslow_list = []

    # Wczytanie strony ze zmiennej url_poslowie
    soup = bs4.BeautifulSoup(requests.get(url_poslowie, verify=True).text, 'html.parser')

    # Wyszukiwanie linków id posłów i ich pobranie
    for link in soup.find_all('a'):
        link = link.get('href')
        if fnmatch.fnmatch(link, url_posla):
            id = link[link.index('id='):link.index('&')].strip('id=')
            id_poslow_list.append(id)

    return id_poslow_list


def get_name(full_name):
    result = None
    while result is None:
        try:
            if full_name.count(' ') == 1:
                return full_name.split(' ')[0]
            elif full_name.count(' ') == 2:
                return ' '.join(full_name.split(' ', 2)[:2])
            elif full_name.count(' ') == 3:
                return full_name.split(' ')[0]
            # else: return full_name.split(' ')[0]

        except Exception as e:
            print(e)
            continue


def get_last_name(full_name):
    result = None
    while result is None:
        try:
            if full_name.count(' ') == 1:
                return full_name.split(' ')[1]
            elif full_name.count(' ') == 2:
                return full_name.split(' ')[2]
            elif full_name.count(' ') == 3:
                return ' '.join(full_name.split(' ')[1:])
            # else: return ' '.join(full_name.split(' ')[:-1])

        except Exception as e:
            print(e)
            continue


# Funkcja do wychywcenia partii
def get_partie():
    print("Sprawdzam nazwy partii...")

    nazwy_partii = []

    # Pobranie ID posiedzeń
    id_posiedzen_list = get_id_posiedzen_list()

    # Iterowanie po każdym posiedzeniu
    for id in id_posiedzen_list:
        url = url_glosowan + id
        print(url)

        # Wczytanie strony z głosowaniami
        soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')

        url = url.strip(id)
        try:
            for link in soup.find_all('a'):
                link = link.get('href')
                if fnmatch.fnmatch(link, url_nr_posiedzenia):
                    link = url_home_link + link

                    # Wczytanie strony z szczegółami głosowań
                    dataframe = pd.read_html(link, encoding='utf-8')[0]
                    partie = dataframe['Klub/Koło'].tolist()

                    # Jeśli partia nie znajduje się już w liście partii, append
                    for partia in partie:
                        if partia not in nazwy_partii: nazwy_partii.append(partia)

                    break
        except Exception as e:
            print(e)
            pass

    print('Pobrane')
    return nazwy_partii


# Funkcja do wychwycenia id, numeru i daty posiedzeń
def get_posiedzenia():
    print("Sprawdzam posiedzenia...")

    miesiace = {
        'stycznia': '01',
        'lutego': '02',
        'marca': '03',
        'kwietnia': '04',
        'maja': '05',
        'czerwca': '06',
        'lipca': '07',
        'sierpnia': '08',
        'września': '09',
        'października': '10',
        'listopada': '11',
        'grudnia': '12'
    }

    id_posiedzen_list = get_id_posiedzen_list()
    try:
        # Wczytanie tabeli ze strony
        dataframe = pd.read_html(url_posiedzen, encoding='utf-8')[0]
        # Usunięcie niepotrzebnych kolumn i zmiana nazwy pozostałych kolumn
        dataframe = dataframe.drop(['Liczba głosowań', 'Unnamed: 3'], axis=1)
        dataframe = dataframe.rename(columns={'Nr pos. Sejmu': 'nr_posiedzenia', 'Data pos. Sejmu': 'data'})

        # Uzupełnienie miejsc NULLow na poprzedzające go wartości, w tym wypadku numery posiedzeń
        dataframe['nr_posiedzenia'] = dataframe['nr_posiedzenia'].fillna(method='ffill')
        dataframe['nr_posiedzenia'] = dataframe['nr_posiedzenia'].astype(int)
        # dataframe = dataframe.sort_values(by='nr_posiedzenia', ignore_index=True)

        # Zwrócenie wszystkich dat w kolumnie 'data' do listy
        date_list = dataframe['data'].tolist()
        new_date_list = []

        # Modyfikacja każdej daty w liście do formatu YYYY-MMMM-DDDD
        for date in date_list:
            date = date.strip(' r.')
            date = date.replace(' ', '-')
            for word, replacment in miesiace.items(): date = date.replace(word, replacment)
            if len(date) == 9: date = '0' + date

            year = date[date.index('-') + 4:]
            month = date[date.index('-'):date.index('-') + 4].strip('-')
            day = date[:date.index('-')]
            date = year + '-' + month + '-' + day

            new_date_list.append(date)

        # Ustawienie nowej kolumny z listy z przekształconymi datami
        date_column = dataframe.columns[1]
        dataframe = dataframe.drop(date_column, axis=1)
        dataframe[date_column] = new_date_list

        # Dodanie kolumny 'id' z poszczególnymi id posiedzień
        dataframe['id'] = id_posiedzen_list
        dataframe = dataframe[['id', 'nr_posiedzenia', 'data']]

        # Zmiana typu kolumny nr_posiedzenia i id ze string na int
        dataframe['nr_posiedzenia'] = dataframe['nr_posiedzenia'].astype(int)
        dataframe['id'] = dataframe['id'].astype(int)
    except Exception as e:
        print(e)

    print('Pobrane')
    # return dataframe.to_csv('posiedzenia.csv', index=False)
    return dataframe


# Funkcja do wychwycenia numerów, opisów głosowań i przypisanie im ich id_posiedzeń
def get_glosowania():
    print("Sprawdzam glosowania...")

    global url_glosowan
    # Utworzenie pustego dataframe'u z kolumnami id_posiedzenia, nr_glosowania, opis
    column_names = ['id_posiedzenia', 'nr_glosowania', 'opis']
    joined_dataframe = pd.DataFrame(columns=column_names)

    id_posiedzen_list = get_id_posiedzen_list()

    # Z listy ID posiedzeń z funkcji get_posiedzenia, przejście po każdym posiedzeniu
    for id in id_posiedzen_list:
        url_glosowan += id
        print(url_glosowan)

        try:
            # Pobranie tabeli z głosowaniami i usunięcie kolumny 'Godzina'
            dataframe = pd.read_html(url_glosowan, encoding='utf-8')[0]
            del dataframe['Godzina']

            # Zmiana nazwy kolumn z 'Nr' na 'nr_glosowania', 'Temat' na 'opis'
            dataframe = dataframe.rename(columns={'Nr': 'nr_glosowania', 'Temat': 'opis'})
            # Wstawienie kolumny w 1 indeks i wartość id_posiedzenia
            dataframe.insert(1, 'id_posiedzenia', id)

            # Dodanie do ostatecznego dataframe'u głosowania z posiedzeń
            joined_dataframe = pd.concat([joined_dataframe, pd.DataFrame.from_records(dataframe)])
            url_glosowan = url_glosowan.strip(id)
        except Exception as e:
            print(e)
            continue

    # Zmiana typu kolumny id_posiedzenia i nr_glosowania ze string na int
    joined_dataframe['id_posiedzenia'] = joined_dataframe['id_posiedzenia'].astype(int)
    joined_dataframe['nr_glosowania'] = joined_dataframe['nr_glosowania'].astype(int)

    print('Pobrane')
    # return joined_dataframe.to_csv('glosowanie.csv', index=False)
    return joined_dataframe


# Funkcja do wychywcenia id, imiona i nazwiska posłów
def get_poslowie():
    print("Sprawdzam posłów...")

    # Wychywcenie ID posłów z linków
    id_poslow_list = get_id_poslow_list()

    column_names = ['id', 'imie', 'nazwisko']
    dataframe = pd.DataFrame(columns=column_names)
    names = []
    last_names = []

    soup = bs4.BeautifulSoup(requests.get(url_poslowie, verify=True).text, 'html.parser')

    # Wychwycenie imion wszystkich posłów
    try:
        for link in soup.find_all('a'):
            link = link.get('href')
            if fnmatch.fnmatch(link, url_posla):

                link = url_home_link2 + link
                print(link)
                soup = bs4.BeautifulSoup(requests.get(link, verify=True).text, 'html.parser')

                for full_name in soup.find_all('h1'):
                    full_name = full_name.get_text()

                    name = get_name(full_name)
                    names.append(name)
                    last_name = get_last_name(full_name)
                    last_names.append(last_name)

        # Ustawienie list jako kolumny w dataframe'ie
        dataframe['id'] = id_poslow_list
        dataframe['imie'] = names
        dataframe['nazwisko'] = last_names
    except Exception as e:
        print(e)
        pass

    print('Pobrane')
    # return dataframe.to_csv('poslowie.csv', index=False)
    return dataframe


# Funkcja do wychwycenia głosów posłów
def get_glosy(id_posla_od, id_posla_do, id_pos_od, id_pos_do):
    print("Sprawdzam głosy...")

    global url_glos_posla
    id_poslow_list = []
    id_posiedzen_list = []

    # Funkcja do wczytania tabeli głosowań z bazy danych, aby pobrać z niej id_głosowań
    def get_database_glosowania():
        sql = '''SELECT * FROM glosowania'''
        table = pd.read_sql(sql, db)
        # db.close()
        return table

    # Funkcja do wczytania tabeli partii z bazy danych, aby pobrać z niej id_partii
    def get_database_partie():
        sql = '''SELECT * FROM partie'''
        table = pd.read_sql(sql, db)
        # db.close()
        return table

    glosowania_database_table = get_database_glosowania()
    partie_database_table = get_database_partie()

    # Funkcja do sprawdzenia w jakiej partii znajdował się poseł podczas oddania swojego głosu
    def check_posel_id_partia(url, name, partie_database_table):
        found = False
        while found is False:
            try:
                soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')
                # Wyszukiwanie głosowania
                for link in soup.find_all('a'):
                    link = link.get('href')
                    if fnmatch.fnmatch(link, url_nr_posiedzenia):
                        link = url_home_link + link
                        # print(link)

                        # Wczytanie głosowania
                        soup = bs4.BeautifulSoup(requests.get(link, verify=True).text, 'html.parser')

                        for partia in soup.find_all('a'):
                            partia = partia.get('href')
                            if fnmatch.fnmatch(partia, url_glosowania_partii):
                                partia_link = url_home_link + partia
                                print(partia_link)
                                nazwa_partii = partia[partia.index('&KodKlubu='):]
                                nazwa_partii = nazwa_partii[nazwa_partii.index('='):].strip('=')

                                dataframe = pd.read_html(partia_link, encoding='utf-8')[0]
                                dataframe_left = dataframe['Nazwisko i imię'].tolist()
                                dataframe_right = dataframe['Nazwisko i imię.1'].tolist()

                                poslowie = dataframe_left + dataframe_right
                                # print(poslowie)
                                # print(name)
                                for posel in poslowie:
                                    if posel == name:
                                        partia_posla = nazwa_partii
                                        found = True
                                        print(full_name + ' ' + partia_posla)
                                        break
                                pass
                            if found: break
                    if found: break
            except Exception as e:
                print(e)
                continue

        # Wczytanie tabeli partii z bazy danych
        partie = partie_database_table
        # Iterowanie po tabeli partii z bazy danych
        for index, row in partie.iterrows():
            if row['nazwa'] == partia_posla:
                id_partii_posla = row['id']
                return id_partii_posla

    column_names = ['id_partia', 'id_posel', 'id_glosowania', 'glos', 'data_glosu']
    joined_dataframe = pd.DataFrame(columns=column_names)

    # Wyszukanie wszystkich id posiedzeń
    full_id_posiedzen_list = get_id_posiedzen_list()
    full_id_posiedzen_list.sort()
    # Ograniczenie wyszukiwania głosowań posłów od jednego posiedzenia do drugiego
    for i in full_id_posiedzen_list[
             full_id_posiedzen_list.index(id_pos_od):full_id_posiedzen_list.index(id_pos_do) + 1]:
        id_posiedzen_list.append(i)

    # Wyszukanie wszystkich id posłów
    full_id_poslow_list = get_id_poslow_list()
    full_id_poslow_list.sort()
    # Ograniczenie wyszukiwania głosowań posłów od jednego ID do drugiego
    for j in full_id_poslow_list[full_id_poslow_list.index(id_posla_od):full_id_poslow_list.index(id_posla_do) + 1]:
        id_poslow_list.append(j)

    for id_posel in id_poslow_list:
        url_glos_posla += id_posel

        for id_pos in id_posiedzen_list:
            counter = 0
            found_glosowanie = False
            temp_pos_link = '*IdDnia=' + id_pos

            while found_glosowanie is False:
                try:
                    # Wczytanie strony głosowania posła
                    soup = bs4.BeautifulSoup(requests.get(url_glos_posla, verify=True).text, 'html.parser')
                    print(url_glos_posla)

                    for link in soup.find_all('a'):
                        link = link.get('href')
                        if fnmatch.fnmatch(link, temp_pos_link):
                            found_glosowanie = True
                            id_glosowan_list = []

                            temp_pos_link = temp_pos_link.strip(id_pos)
                            id_posiedzenia = link[link.index('IdDnia='):].strip('IdDnia=')

                            temp_link = url_home_link + link
                            print(temp_link)

                            soup = bs4.BeautifulSoup(requests.get(temp_link, verify=True).text, 'html.parser')

                            header_tag = soup.find('h1').get_text()
                            full_name = header_tag[:header_tag.index('Głosowania')]

                            name = get_name(full_name)
                            last_name = get_last_name(full_name)
                            new_full_name = last_name + ' ' + name

                            date = header_tag[header_tag.index('dniu '):header_tag.index(' na')].strip('dniu ')

                            year = date[date.index('-') + 4:]
                            month = date[date.index('-'):date.index('-') + 4].strip('-')
                            day = date[:date.index('-')]
                            date = year + '-' + month + '-' + day

                            id_partii_posla = check_posel_id_partia(temp_link, new_full_name, partie_database_table)

                            # Dataframe danych z głosowania posła na danym posiedzeniu
                            dataframe = pd.read_html(temp_link, encoding='utf-8')[0]

                            # Usunięcie kolumny 'Godzina' z dataframe'u
                            del dataframe['Godzina']
                            # Wstawienie kolumny 'id_partia' i 'id_posel' z ich ID
                            dataframe.insert(0, 'id_partia', id_partii_posla)
                            dataframe.insert(1, 'id_posel', id_posel)
                            # Zmiana nazw kolumn i usunięcie niepotrzebnego ostatniego wiersza z tabeli
                            dataframe = dataframe.rename(
                                columns={'Numer': 'nr_glosowania', 'Wynik': 'glos', 'Temat': 'opis'})
                            dataframe = dataframe[:-1]

                            # Iterowanie po tabeli głosowań z bazy danych
                            for index1, row_glosowania in glosowania_database_table.iterrows():
                                if row_glosowania['id_posiedzenia'] == int(id_posiedzenia):
                                    id_glosowania = row_glosowania['id']
                                    opis = row_glosowania['opis']
                                    numer_glosowania = row_glosowania['nr_glosowania']

                                    # Iterowanie po aktualnym dataframie w celu przypisania id_glosowania głosowaniom
                                    for index2, row_dataframe in dataframe.iterrows():
                                        numer_glosowania2 = row_dataframe['nr_glosowania']
                                        opis2 = row_dataframe['opis']

                                        # Jeśli numer głosowania i opis są takie same jak w tabeli z bazy danych,
                                        # dodanie id_glosowania do listy głosowań
                                        if numer_glosowania == int(numer_glosowania2) and opis == opis2:
                                            id_glosowan_list.append(id_glosowania)

                            # Usunięcie kolumny opis, nr_glosowania i wstawienie kolumny 'id_głosowania' z listą id głosowań,
                            # kolumny data_glosu i wypełnienie kolumny datą głosu
                            del dataframe['opis']
                            del dataframe['nr_glosowania']
                            dataframe.insert(2, 'id_glosowania', id_glosowan_list)
                            dataframe.insert(3, 'data_glosu', date)
                            dataframe['data_glosu'] = dataframe['data_glosu'].fillna(method='ffill')

                            # Przyłączenie danych z aktualnego dataframe'u głosów posła do ostatecznej tabeli
                            joined_dataframe = pd.concat([joined_dataframe, pd.DataFrame.from_records(dataframe)])

                    if found_glosowanie is False:
                        print('Nie wczytano głosowania posła, wczytuję jeszcze raz')
                        counter += 1
                        if counter == 3:
                            print('Poseł nie był na tym posiedzeniu')
                            found_glosowanie = True
                            break
                        continue

                except Exception as e:
                    print(e)
                    continue

        url_glos_posla = url_glos_posla.strip(id_posel)

    print('Pobrane')
    # joined_dataframe.to_csv('glosy.csv', index=False)
    return joined_dataframe

# start = time.time()
# get_partie()
# get_posiedzenia()
# get_glosowania()
# get_poslowie()
# get_glosy()
# end = time.time()
# print("Zajęło: " + str((end-start)/60))