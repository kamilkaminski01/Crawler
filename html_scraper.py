import requests
import bs4
import fnmatch
import pandas as pd
import os
import time

urls = [] # Lista stron głosowań
url_links = [] # Lista wszystkich linków ze stron głosowań
vote_links = [] # Lista glosowan posłów partii na glosowaniu

# Partie w 9 kadencji sejmu 2019-2023
PiS = [] # PiS, Prawo i Sprawiedliwosc
KO = [] # KO, Koalicja Obywatelska
Lewica = [] # Lewica
KP = [] # KP, Koalicja Polska
SLD = [] # SLD, Sojusz Lewicy Demokratycznej
PSL = [] # PSL, Polskie Stronnictwo Ludowe
PSL_Kukiz = [] #
Kukiz = [] # Kukiz'15
Konfederacja = [] # Konfederacja
Polska = [] # Polska2050
Porozumienie = [] # Porozumienie, Porozumienie Jaroslawa Gowina
PPS = [] # PPS, Polska Parta Socjalistyczna
PS = [] # PS, Polskie Sprawy
niez = []

# Funckja do przekształcenia tabeli i pobranie jej do pliku csv
def to_csv(url, partia, nr_posiedzenia, nr_glosowania):
    # Pobranie tabeli o zerowym indeksie ze strony. 'encoding' ważne, aby przeczytać polskie znaki
    dataframe = pd.read_html(url, encoding='utf-8')[0]

    # Usuniecie z pierwszej(lewej) części tabeli drugą(prawą) część tabeli
    dataframe_left = dataframe.drop(['Lp..1', 'Nazwisko i imię.1', 'Głos.1'], axis=1)

    # Ustawienie drugą część tabeli i zmiana nazwy kolumn, aby można bylo dołączyć do siebie obie części
    dataframe_right = dataframe[['Lp..1', 'Nazwisko i imię.1', 'Głos.1']]
    dataframe_right = dataframe_right.rename(columns={'Lp..1': 'Lp.', 'Nazwisko i imię.1': 'Nazwisko i imię', 'Głos.1': 'Głos'})

    # Utworzenie jednej tabeli, posortowanie po 'Lp.', usunięcie wierszy które mają same NULLe i
    # ustawienie kolumny 'Lp.' z floatów na inty
    joined_dataframe = dataframe_left.append(dataframe_right)
    joined_dataframe = joined_dataframe.sort_values(by='Lp.', ignore_index=True)
    joined_dataframe = joined_dataframe.dropna(how='all')
    joined_dataframe['Lp.'] = joined_dataframe['Lp.'].astype(int)

    # Podzielenie kolumny Nazwisko i imię na kolumne nazwisko i kolumnę imię
    joined_dataframe[['Nazwisko', 'Imie']] = joined_dataframe['Nazwisko i imię'].str.split(' ', 1, expand=True)
    del joined_dataframe['Nazwisko i imię']
    joined_dataframe = joined_dataframe[['Lp.','Nazwisko', 'Imie', 'Głos']]

    # Zapisanie tabeli do pliku csv bez indeksu z tytulem header
    header = 'glosowanie' + partia + str(nr_posiedzenia) + '_' + str(nr_glosowania) + '.csv'
    path = '/Users/kamilkaminski/Downloads/Scraping/'

    if not os.path.exists(path): os.makedirs(path)
    os.chdir(path)

    return joined_dataframe.to_csv(header, encoding='utf-8', index=False)


# Zapisanie wszystkich linków głosowań z posiedzeń do listy urls
def get_urls(posiedzenia, glosowania):
    for i in range(1, posiedzenia+1):
        url_string_new = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=' + str(i) + '&NrGlosowania='
        url_string_old = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=' + str(i) + '&NrGlosowania='

        for j in range(1, glosowania+1):
            url_string_new += str(j)

            # Wczytanie strony
            soup = bs4.BeautifulSoup(requests.get(url_string_new, verify=True).text, 'html.parser')

            # Wyszukiwanie na stronie linku z klasą 'pdf' i dodanie jej do listy urls
            for link in soup.find_all(class_='pdf'):
                print(url_string_new)
                urls.append(url_string_new)

            # Jeśli nie znaleziono linku z klasą 'pdf' na stronie, koniec pętli i przejście do następnego posiedzenia
            if link not in soup.find_all(class_='pdf'): break
            url_string_new = url_string_old


def get_voting():
    home_link = 'https://www.sejm.gov.pl/Sejm9.nsf/'

    for url in urls:
        # Wczytanie strony
        soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')

        nr_posiedzenia = url[url.index('NrPosiedzenia='):url.index('&NrGlosowania')].strip("NrPosiedzenia=")
        nr_glosowania = url[url.index('NrGlosowania='):].strip("NrGlosowania=")

        # Wyszukiwanie i połączenie opisów głosowań
        opis_glosowania_list = []
        for p in soup.find_all(class_='subbig'): opis_glosowania_list.append(p.get_text())
        opis_glosowania = ' - '.join(opis_glosowania_list)

        # Wyszukiwanie na stronie wszystkich linków i dodanie do listy linków
        for link in soup.find_all('a'): url_links.append(link.get('href'))

        # Wyszukiwanie na stronie linku z głosowania danej partii
        for link in url_links:
            if fnmatch.fnmatch(link, '*agent.xsp?symbol=klubglos&IdGlosowania=*'): vote_links.append(link)

        # Filtrowanie linków do poszczególnych list partii
        for link in vote_links:
            while True:
                try:
                    link = home_link + link
                    if fnmatch.fnmatch(link, '*KodKlubu=PiS'):
                        PiS.append(link)
                        partia = 'PiS'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=KO'):
                        KO.append(link)
                        partia = 'KO'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=Lewica'):
                        Lewica.append(link)
                        partia = 'Lewica'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=SLD'):
                        partia = 'SLD'
                        SLD.append(link)
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=PSL'):
                        PSL.append(link)
                        partia = 'PSL'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=PSL-Kukiz15'):
                        PSL_Kukiz.append(link)
                        partia = 'PSL-Kukiz'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=Kukiz15'):
                        Kukiz.append(link)
                        partia = 'Kukiz15'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=Konfederacja'):
                        Konfederacja.append(link)
                        partia = 'Konfederacja'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=KP'):
                        KP.append(link)
                        partia = 'KP'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=Polska2050'):
                        Polska.append(link)
                        partia = 'Polska'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=Porozumienie'):
                        Porozumienie.append(link)
                        partia = 'Porozumienie'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=PPS'):
                        PPS.append(link)
                        partia = 'PPS'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=PS'):
                        PS.append(link)
                        partia = 'PS'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)
                    elif fnmatch.fnmatch(link, '*KodKlubu=niez.'):
                        niez.append(link)
                        partia = 'niez'
                        to_csv(link, partia, nr_posiedzenia, nr_glosowania)

                # Powtórzenie dodania linku w przypadku błędu ConnectionResetError po 3 sekundach
                except(NameError, AttributeError, ConnectionResetError):
                    print("Rozłączyło połącznie, ponawiam pobranie")
                    time.sleep(3)
                    continue
                break


posiedzenia = 1
glosowania = 1
get_urls(posiedzenia, glosowania)

print("Sprawdzam i pobieram glosowania partii...")
start_time = time.time()
get_voting()
print("Pobrane")
print("Zajelo: ",time.time() - start_time)



"""
print(PiS[1])
print(KO[1])
print(Lewica[1])
print(KP[1])
print(SLD[1])
print(PSL[1])
print(PSL_Kukiz[1])
print(Kukiz[1])
print(Konfederacja[1])
print(Polska[1])
print(Porozumienie[1])
print(PPS[1])
print(PS[1])
print(niez[1])
"""


