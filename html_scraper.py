import requests
import bs4
import fnmatch
import pandas as pd
import os
import time
import mysql_database as mysql

partie = [
    '*KodKlubu=PiS',
    '*KodKlubu=KO',
    '*KodKlubu=Lewica',
    '*KodKlubu=SLD',
    '*KodKlubu=PSL',
    '*KodKlubu=PSL-Kukiz15',
    '*KodKlubu=Kukiz15',
    '*KodKlubu=Konfederacja',
    '*KodKlubu=KP',
    '*KodKlubu=Polska2050',
    '*KodKlubu=Porozumienie',
    '*KodKlubu=PPS',
    '*KodKlubu=PS',
    '*KodKlubu=niez.'
]

partie_sql = []
opisy_sql = []

# Lista stron głosowań
urls = []

url_posiedzenia = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia='
url_glosowania = '&NrGlosowania='
path = '/Users/kamilkaminski/Downloads/Scraping/'
home_link = 'https://www.sejm.gov.pl/Sejm9.nsf/'

# Funkcja do wychwycenia nazwy partii
def get_partie(partia):
    nazwa = partia[partia.index("*KodKlubu="):]
    nazwa = nazwa[nazwa.index("="):].strip("=")

    return nazwa

# Funkcja do wyszukiwania i połączenia opisów głosowań
def get_opis(soup):
    list = []
    for p in soup.find_all(class_='subbig'): list.append(p.get_text())
    opis_glosowania = ' - '.join(list)

    return opis_glosowania

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

    # Usuniecie z pierwszej(lewej) części tabeli drugą(prawą) część tabeli
    dataframe_left = dataframe.drop(['Lp..1', 'Nazwisko i imię.1', 'Głos.1'], axis=1)

    # Ustawienie drugą część tabeli i zmiana nazwy kolumn, aby można bylo dołączyć do siebie obie części
    dataframe_right = dataframe[['Lp..1', 'Nazwisko i imię.1', 'Głos.1']]
    dataframe_right = dataframe_right.rename(columns={'Lp..1': 'Lp.', 'Nazwisko i imię.1': 'Nazwisko i imię', 'Głos.1': 'Głos'})

    # Utworzenie jednej tabeli, posortowanie po 'Lp.', usunięcie wierszy które mają same NULLe i
    # ustawienie kolumny 'Lp.' z floatów na inty
    joined_dataframe = pd.concat([dataframe_left, dataframe_right])
    joined_dataframe = joined_dataframe.sort_values(by='Lp.', ignore_index=True)
    joined_dataframe = joined_dataframe.dropna(how='all')
    joined_dataframe['Lp.'] = joined_dataframe['Lp.'].astype(int)

    # Podzielenie kolumny Nazwisko i imię na kolumne nazwisko i kolumnę imię
    joined_dataframe[['Nazwisko', 'Imie']] = joined_dataframe['Nazwisko i imię'].str.split(' ', 1, expand=True)
    del joined_dataframe['Nazwisko i imię']
    joined_dataframe = joined_dataframe[['Lp.','Nazwisko', 'Imie', 'Głos']]

    # Zapisanie tabeli do pliku csv bez indeksu z tytulem header
    header = nazwa_partii + '-' + str(nr_posiedzenia) + '_' + str(nr_glosowania) + '.csv'

    if not os.path.exists(path): os.makedirs(path)
    os.chdir(path)

    return joined_dataframe.to_csv(header, encoding='utf-8', index=False)
    # return joined_dataframe

# Zapisanie wszystkich linków głosowań z posiedzeń do listy urls
def get_urls(posiedzenia, glosowania):
    for i in range(39, posiedzenia+1):

        # Zmienna do zweryfkiwania przeskoku głosowania, np. głosowanie 41, głosowanie 42, głosowanie 44
        verifier = 0

        url_string_old = url_posiedzenia + str(i) + url_glosowania
        url_string_new = url_posiedzenia + str(i) + url_glosowania

        for j in range(1, glosowania+1):
            url_string_new += str(j)

            # Wczytanie strony
            soup = bs4.BeautifulSoup(requests.get(url_string_new, verify=True).text, 'html.parser')

            # Wyszukiwanie na stronie linku z klasą 'pdf' i dodanie jej do listy urls
            for link in soup.find_all(class_='pdf'):
                print(url_string_new)
                urls.append(url_string_new)
                # Jeśli nie znaleziono linku z klasą 'pdf' na stronie, zwiększenie zmiennej verifier o 1
                if link not in soup.find_all(class_='pdf'): verifier += 1

            # Jeśli po 5 próbach nie znaleziono kolejnej strony, koniec poszukiwania na danym posiedzeniu
            if verifier == 5: break
            url_string_new = url_string_old

def get_voting():
    for url in urls:
        url_links = []  # Lista wszystkich linków ze stron głosowań
        vote_links = []  # Lista glosowan posłów partii na glosowaniu

        # Wczytanie strony
        soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')

        nr_posiedzenia = url[url.index('NrPosiedzenia='):url.index('&NrGlosowania')].strip("NrPosiedzenia=")
        nr_glosowania = url[url.index('NrGlosowania='):].strip("NrGlosowania=")

        # Wychywcenie opisów głosowań
        opis = get_opis(soup)
        opisy_sql.append(opis)

        # Wyszukiwanie na stronie wszystkich linków i dodanie do listy linków
        for link in soup.find_all('a'): url_links.append(link.get('href'))

        # Wyszukiwanie na stronie linku z głosowania danej partii
        for link in url_links:
            if fnmatch.fnmatch(link, '*agent.xsp?symbol=klubglos&IdGlosowania=*'): vote_links.append(link)

        # Filtrowanie linków do poszczególnych list partii
        for link in vote_links:
            while True:
                try:
                    temp_link = home_link + link
                    for partia in partie:
                        if fnmatch.fnmatch(temp_link, partia):
                            # Wychwycenie nazwy partii
                            nazwa_partii = get_partie(partia)

                            print("Pobieram partie: posiedzenie "+nr_posiedzenia+" glosowanie "+nr_glosowania+ " partia "+nazwa_partii)
                            get_dataframe(temp_link, nazwa_partii, nr_posiedzenia, nr_glosowania)

                # Powtórzenie dodania linku w przypadku błędu ConnectionResetError po 6 sekundach
                except(NameError, AttributeError, ConnectionResetError):
                    print("Rozłączyło połączenie, ponawiam pobranie")
                    time.sleep(6)
                    continue
                break


posiedzenia = 10
glosowania = 2
get_urls(posiedzenia, glosowania)

print("Sprawdzam i pobieram glosowania partii...")
get_voting()
print("Pobrane")

# start_time = time.time()
# print("Zajelo: ",time.time() - start_time)