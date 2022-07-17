import requests
import bs4
import fnmatch
import pandas as pd
import os
import time

partie = [
    'PiS',
    'KO',
    'Lewica',
    'SLD',
    'PSL',
    'PSL-Kukiz15',
    'Kukiz15',
    'Konfederacja',
    'KP',
    'Polska2050',
    'Porozumienie',
    'PPS',
    'PS',
    'niez.'
]

# sql_list_opisy = []
sql_list_daty_glosowan = []

urls = [] # Lista stron głosowań
id_posiedzen_list = [] # Lista ID posiedzeń

url_nr_posiedzenia = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia='
url_nr_glosowania = '&NrGlosowania='
path = '/Users/kamilkaminski/Downloads/Scraping/'
url_home_link = 'https://www.sejm.gov.pl/Sejm9.nsf/'
url_glosowania_partii = '*agent.xsp?symbol=klubglos&IdGlosowania=*'
url_posiedzen = 'https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=posglos&NrKadencji=9'
url_glosowan = 'https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=listaglos&IdDnia='
url_poslowie = 'https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=C'

# Funkcja do wychwycenia id, numeru i daty posiedzeń
def get_posiedzenia():
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

    # Wczytanie strony ze zmiennej url_posiedzen
    soup = bs4.BeautifulSoup(requests.get(url_posiedzen, verify=True).text, 'html.parser')

    # Wyszukiwanie linków dat posiedzeń i pobranie od nich ID
    for link in soup.find_all('a'):
        link = link.get('href')
        if fnmatch.fnmatch(link, '*IdDnia=*'):
            link = link[link.index('IdDnia='):].strip('IdDnia=')
            id_posiedzen_list.append(link)

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
        if len(date) == 9: date = '0'+date

        year = date[date.index('-')+4:]
        month = date[date.index('-'):date.index('-')+4].strip('-')
        day = date[:date.index('-')]
        date = year + '-' + month + '-' + day

        new_date_list.append(date)

    # Ustawienie nowej kolumny z listy z przekształconymi datami
    date_column = dataframe.columns[1]
    dataframe = dataframe.drop(date_column, axis=1)
    dataframe[date_column] = new_date_list

    # Dodanie kolumny 'id_posiedzenia' z poszczególnymi id posiedzień
    dataframe['id_posiedzenia'] = id_posiedzen_list
    dataframe = dataframe[['id_posiedzenia', 'nr_posiedzenia', 'data']]

    # Zmiana typu kolumny nr_posiedzenia i id_posiedzenia ze string na int
    dataframe['nr_posiedzenia'] = dataframe['nr_posiedzenia'].astype(int)
    dataframe['id_posiedzenia'] = dataframe['id_posiedzenia'].astype(int)

    # return dataframe.to_csv('posiedzenia.csv', index=False)
    return dataframe

# Funkcja do wychwycenia numerów, opisów głosowań i przypisanie im ich id_posiedzeń
def get_glosowania():
    global url_glosowan
    # Utworzenie pustego dataframe'u z kolumnami id_posiedzenia, nr_glosowania, opis
    # column_names = ['id_glosowania', 'id_posiedzenia', 'nr_glosowania', 'opis']
    column_names = ['id_posiedzenia', 'nr_glosowania', 'opis']
    joined_dataframe = pd.DataFrame(columns=column_names)

    # Z listy ID posiedzeń z funkcji get_posiedzenia, przejście po każdym posiedzeniu
    for id in id_posiedzen_list:
        url_glosowan += id

        # Pobranie tabeli z głosowaniami i usunięcie kolumny 'Godzina'
        dataframe = pd.read_html(url_glosowan, encoding='utf-8')[0]
        del dataframe['Godzina']

        # Zmiana nazwy kolumn z 'Nr' na 'nr_glosowania', 'Temat' na 'opis'
        dataframe = dataframe.rename(columns={'Nr': 'nr_glosowania', 'Temat': 'opis'})
        # Wstawienie w kolumnie o 0-owym indeksie id posiedzenia
        dataframe.insert(1, 'id_posiedzenia', id)

        # Dodanie do ostatecznego dataframe'u głosowania z posiedzeń
        # joined_dataframe = joined_dataframe.append(dataframe)
        joined_dataframe = pd.concat([joined_dataframe, pd.DataFrame.from_records(dataframe)])
        url_glosowan = url_glosowan.strip(id)

    # Zmiana typu kolumny id_posiedzenia i nr_glosowania ze string na int
    joined_dataframe['id_posiedzenia'] = joined_dataframe['id_posiedzenia'].astype(int)
    joined_dataframe['nr_glosowania'] = joined_dataframe['nr_glosowania'].astype(int)

    # return joined_dataframe.to_csv('glosowanie.csv', index=False)
    return joined_dataframe

#
def get_date(soup):
    for small in soup.find_all('small'):
        full_date = small.get_text().strip('dnia ')
        date = full_date[:full_date.index(' r.')]

        year = date[date.index('-')+4:]
        month = date[date.index('-'):date.index('-')+4].strip('-')
        day = date[:date.index('-')]

        date = year+'-'+month+'-'+day
        # hour = full_date[full_date.index('godz. '):].strip('godz. ')
    sql_list_daty_glosowan.append(date)
    return date

# Funkcja do wychywcenia posłów
def get_poslowie():
    soup = bs4.BeautifulSoup(requests.get(url_poslowie, verify=True).text, 'html.parser')

    for posel in soup.find_all(class_='deputyName'):
        posel = posel.get_text()
        print(posel)




# Funkcja do przekształcenia innego radzaju występującej tabeli
def get_dataframe_other(url, nazwa_partii, nr_posiedzenia, nr_glosowania):
    # Pobranie tabeli o pierwszym indeksie ze strony
    dataframe = pd.read_html(url)[1]
    # dataframe_nie_glos = pd.read_html(url)[2]

    # Usunięcie wierszy które mają same NULLe i ustawienie kolumny 'Lp.' z floatów na inty
    dataframe = dataframe.dropna(how='all')
    dataframe['Lp.'] = dataframe['Lp.'].astype(int)

    # Podzielenie kolumny 'Nazwisko i imię posła' na dwie oddzielne 'Nazwisko' i 'Imię'
    dataframe[['Nazwisko', 'Imie']] = dataframe['Nazwisko i imię posła'].str.split(' ', 1, expand=True)
    del dataframe['Nazwisko i imię posła']

    # Ustawienie kolumn w kolejności: 'Lp.' 'Nazwisko' 'Imie', ...
    cols = dataframe.columns.tolist()
    cols.remove('Lp.')
    cols.remove('Nazwisko')
    cols.remove('Imie')
    cols.insert(0,'Lp.')
    cols.insert(1,'Nazwisko')
    cols.insert(2,'Imie')

    dataframe = dataframe[cols]

    # Posłowie którzy nie byli obecni na głosowaniu, czyli kolejna tabela pod główną tabelą
    # dataframe_nie_glos_left = dataframe_nie_glos[['0']]
    # dataframe_nie_glos_right = dataframe_nie_glos[['1']]
    # dataframe_nie_glos_joined = pd.concat(dataframe_nie_glos_left,dataframe_nie_glos_right)
    # print(dataframe_nie_glos_joined)
    # print(dataframe_nie_glos.columns.tolist())
    # print(dataframe_nie_glos.info())
    # dataframe_nie_glos = dataframe_nie_glos[cols]

    # Zapisanie tabeli do pliku csv bez indeksu z tytulem header

    header = 'glosowanie' + nazwa_partii + str(nr_posiedzenia) + '_' + str(nr_glosowania) + '.csv'

    path = '/Users/kamilkaminski/Downloads/Scraping/'
    if not os.path.exists(path): os.makedirs(path)
    os.chdir(path)
    return dataframe.to_csv(header, encoding='utf-8', index=False)

# Funckja do przekształcenia tabeli
def get_dataframe(url, nazwa_partii, nr_posiedzenia, nr_glosowania):
    # Pobranie tabeli o zerowym indeksie ze strony. 'encoding' ważne, aby przeczytać polskie znaki
    dataframe = pd.read_html(url, encoding='utf-8')[0]

    # Usuniecie z pierwszej(lewej) części tabeli drugą(prawą) część tabeli i zmiana nazwy kolumn
    dataframe_left = dataframe.drop(['Lp..1', 'Nazwisko i imię.1', 'Głos.1'], axis=1)
    dataframe_left = dataframe_left.rename(columns={'Nazwisko i imię': 'nazwisko i imie', 'Głos': 'glos'})

    # Ustawienie drugą część tabeli i zmiana nazwy kolumn, aby można bylo dołączyć do siebie obie części
    dataframe_right = dataframe[['Lp..1', 'Nazwisko i imię.1', 'Głos.1']]
    dataframe_right = dataframe_right.rename(columns={'Lp..1': 'Lp.', 'Nazwisko i imię.1': 'nazwisko i imie', 'Głos.1': 'glos'})

    # Utworzenie jednej tabeli, posortowanie po 'Lp.', usunięcie wierszy które mają same NULLe i
    # ustawienie kolumny 'Lp.' z floatów na inty
    joined_dataframe = pd.concat([dataframe_left, dataframe_right])
    joined_dataframe = joined_dataframe.sort_values(by='Lp.', ignore_index=True)
    joined_dataframe = joined_dataframe.dropna(how='all')
    joined_dataframe['Lp.'] = joined_dataframe['Lp.'].astype(int)

    # Podzielenie kolumny Nazwisko i imię na kolumne nazwisko i kolumnę imię
    joined_dataframe[['nazwisko', 'imie']] = joined_dataframe['nazwisko i imie'].str.split(' ', 1, expand=True)
    del joined_dataframe['nazwisko i imie']
    joined_dataframe = joined_dataframe[['Lp.','nazwisko', 'imie', 'glos']]

    # Zapisanie tabeli do pliku csv bez indeksu z tytulem header
    header = nazwa_partii + '-' + str(nr_posiedzenia) + '_' + str(nr_glosowania) + '.csv'

    if not os.path.exists(path): os.makedirs(path)
    os.chdir(path)

    return joined_dataframe.to_csv(header, encoding='utf-8', index=False)

# Zapisanie wszystkich linków głosowań z posiedzeń do listy urls
def get_urls(posiedzenia, glosowania):
    for i in range(1, posiedzenia+1):
        # Zmienna do zweryfkiwania przeskoku głosowania, np. głosowanie 41, głosowanie 42, głosowanie 44
        verifier = 0

        url_old = url_nr_posiedzenia + str(i) + url_nr_glosowania
        url_new = url_nr_posiedzenia + str(i) + url_nr_glosowania

        for j in range(1, glosowania+1):
            url_new += str(j)

            # Wczytanie strony
            soup = bs4.BeautifulSoup(requests.get(url_new, verify=True).text, 'html.parser')

            # Wyszukiwanie na stronie linku z klasą 'pdf' i dodanie jej do listy urls
            for link in soup.find_all(class_='pdf'):
                print(url_new)
                urls.append(url_new)
                # Jeśli nie znaleziono linku z klasą 'pdf' na stronie, zwiększenie zmiennej verifier o 1
                if link not in soup.find_all(class_='pdf'): verifier += 1

            # Jeśli po 5 próbach nie znaleziono kolejnej strony, koniec poszukiwania na danym posiedzeniu
            if verifier == 5: break
            url_new = url_old

#
def get_voting():
    for url in urls:
        vote_links = []  # Lista głosowań posłów partii na głosowaniu

        # Wczytanie strony
        soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')

        nr_posiedzenia = url[url.index('NrPosiedzenia='):url.index('&NrGlosowania')].strip("NrPosiedzenia=")
        nr_glosowania = url[url.index('NrGlosowania='):].strip("NrGlosowania=")

        # Wychywcenie opisu i daty głosowania
        # opis = get_opis(soup)
        # data = get_date(soup)

        # Wyszukiwanie na stronie wszystkich linków z głosowań partii i dodanie do listy linków
        for link in soup.find_all('a'):
            link = link.get('href')
            if fnmatch.fnmatch(link, url_glosowania_partii): vote_links.append(link)

        # Filtrowanie linków do poszczególnych głosowań partii
        for link in vote_links:
            while True:
                try:
                    temp_link = url_home_link + link
                    for partia in partie:
                        temp_partia = '*' + partia
                        if fnmatch.fnmatch(temp_link, temp_partia):
                            print("Pobieram partie: "+partia+" posiedzenie: "+nr_posiedzenia+" glosowanie: "+nr_glosowania)
                            get_dataframe(temp_link, partia, nr_posiedzenia, nr_glosowania)
                # Powtórzenie dodania linku w przypadku błędu ConnectionResetError po 5 sekundach
                except(NameError, AttributeError, ConnectionResetError):
                    print("Rozłączyło połączenie, ponawiam pobranie")
                    time.sleep(5)
                    continue
                break


posiedzenia = 2
glosowania = 1

# get_urls(posiedzenia, glosowania)
# get_posiedzenia()
# get_glosowania()
# get_voting()
get_poslowie()