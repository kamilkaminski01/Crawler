import pandas as pd
import os

# Ustawienie ograniczen na wyswietlenie kolumn i wierszy na brak
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def to_csv(url, nr_posiedzenia, nr_glosowania):
    # Pobranie danych z linku, 'encoding' wazne, aby przeczytac polskie znaki
    df = pd.read_html(url, encoding='utf-8')[0]

    # Usuniecie z pierwszej części tabeli, drugą część tabeli
    df1 = df.drop(['Lp..1', 'Nazwisko i imię.1', 'Głos.1'], axis=1)

    # Ustawienie drugą część tabeli i zmiana nazwy kolumn, aby mozna bylo dołączyć do siebie obie części
    df2 = df[['Lp..1', 'Nazwisko i imię.1', 'Głos.1']]
    df2 = df2.rename(columns={'Lp..1': 'Lp.', 'Nazwisko i imię.1': 'Nazwisko i imię', 'Głos.1': 'Głos'})

    # Utworzenie jednej tabeli, posortowanie po 'Lp.', usunięcie wierszy które mają same NULLe i
    # ustawienie kolumny 'Lp.' z floatów na inty
    new_df = df1.append(df2)
    new_df = new_df.sort_values(by='Lp.', ignore_index=True)
    new_df = new_df.dropna(how='all')
    new_df['Lp.'] = new_df['Lp.'].astype(int)

    # Zapisanie tabeli do pliku csv bez indeksu z tytulem header
    header = 'glosowanie' + str(nr_posiedzenia) + '_' + str(nr_glosowania) + '.csv'
    path = '/Users/kamilkaminski/Downloads/Scraping/'

    if not os.path.exists(path): os.makedirs(path)
    os.chdir(path)

    return new_df.to_csv(header, encoding='utf-8', index=False)


url = 'https://sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=klubglos&IdGlosowania=53744&KodKlubu=PiS'

to_csv(url,2,3)
print("Zapisane")