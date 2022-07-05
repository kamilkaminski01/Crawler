import requests
import bs4
import os
import urllib.request
import fnmatch

urls = [] # Lista stron glosowan
list_link = [] # Lista wszystkich linkow ze stron glosowan1


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


# Zapisanie wszystkich linkow z poszczegolnymi posiedzeniami oraz glosowaniami na posiedzaniach do listy
# def get_urls(posiedzenia, glosowania):
#     for i in range(1, posiedzenia + 1):
#         url_string_new = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=' + str(i) + '&NrGlosowania='
#         url_string_old = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=' + str(i) + '&NrGlosowania='
#
#         for j in range(1, glosowania + 1):
#             url_string_new += str(j)
#             urls.append(url_string_new)
#             url_string_new = url_string_old


# for link in soup.find_all('a'):
#     list_link.append(link.get('href'))


# for link in list_link:
#     if fnmatch.fnmatch(link, 'http://orka.sejm.gov.pl*'):
#         urls.append(url_string_new)
#         url_string_new = url_string_old
#     else:
#         pass


def get_urls(posiedzenia, glosowania):
    for i in range(1, posiedzenia + 1):
        url_string_new = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=' + str(i) + '&NrGlosowania='
        url_string_old = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=' + str(i) + '&NrGlosowania='

        for j in range(1, glosowania + 1):
            url_string_new += str(j)

            print(url_string_new)
            soup = bs4.BeautifulSoup(requests.get(url_string_new, verify=True).text, 'html.parser')

            for link in soup.find_all(class_='pdf'):
                urls.append(url_string_new)

            if link not in soup.find_all(class_='pdf'):
                break

            url_string_new = url_string_old


posiedzenia = 3
glosowania = 10

get_urls(posiedzenia, glosowania)


home_link = 'https://www.sejm.gov.pl/Sejm9.nsf/'

for url in urls:
    soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')

    nr_posiedzenia = url[url.index('NrPosiedzenia='):url.index('&NrGlosowania')].strip("NrPosiedzenia=")
    nr_glosowania = url[url.index('NrGlosowania='):].strip("NrGlosowania=")

    for link in soup.find_all('a'):
        list_link.append(link.get('href'))

    for link in list_link:
        try:
            link = home_link+link
            if fnmatch.fnmatch(link, '*KodKlubu=PiS'):
                PiS.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=KO'):
                KO.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=Lewica'):
                Lewica.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=SLD'):
                SLD.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=PSL'):
                PSL.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=PSL-Kukiz15'):
                PSL_Kukiz.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=Kukiz15'):
                Kukiz.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=Konfederacja'):
                Konfederacja.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=KP'):
                KP.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=Polska2050'):
                Polska.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=Porozumienie'):
                Porozumienie.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=PPS'):
                PPS.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=PS'):
                PS.append(link)
            elif fnmatch.fnmatch(link, '*KodKlubu=niez.'):
                niez.append(link)

        except(NameError, AttributeError):
            pass


for url in PiS:
    print(url)