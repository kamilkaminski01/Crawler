import requests
import bs4
import os
import urllib.request
import fnmatch

posiedzenia = int(input("Podaj liczbe posiedzen: "))
glosowania = int(input("Podaj ogolna liczbe glosowan na posiedzeniach: "))
urls = []

# Zapisanie wszystkich linkow z poszczegolnymi posiedzeniami oraz glosowaniami na posiedzaniach do listy
for i in range(1, posiedzenia+1):
    url_string_new = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=' + str(i) + '&NrGlosowania='
    url_string_old = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=' + str(i) + '&NrGlosowania='

    for j in range(1, glosowania+1):
        url_string_new += str(j)
        urls.append(url_string_new)
        url_string_new = url_string_old

# Przejscie wszystkich linkow na podanej stronie
for url in urls:
    soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')

    # Zapis wszystkich linkow na aktualnej stronie do listy
    list_link = []
    for link in soup.find_all('a'):
        list_link.append(link.get('href'))

    # Wyszukiwanie linku(w tym przypadku pdfa) z nazwa "orka.sejm.gov.pl itd."
    for link in list_link:
        try:
            if fnmatch.fnmatch(link, 'http://orka.sejm.gov.pl*'):
                print(link)

                # Wycinek stringa - od znalezienia znaku '&' do konca stringa
                number = link[link.index('&'):]

                # Zapis do folderu
                path = '/Users/kamilkaminski/Downloads/Scraping/'
                file_name = link.replace(link, 'glosowanie') + number + '.pdf'
                path_file_join = os.path.join(os.path.dirname(path), file_name)
                urllib.request.urlretrieve(link, path_file_join)
        except(NameError, AttributeError):
            pass


print("Pomyslnie zapisane")