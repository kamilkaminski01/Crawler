import fnmatch

import bs4
import pandas as pd
import requests  # type: ignore

from urls_variables import (url_deputies, url_deputy, url_home_link,
                            url_home_link2, url_nr_sitting, url_party_voting,
                            url_sitting, url_voting)
from utils import (get_id_deputies_list, get_id_sittings_list, get_last_name,
                   get_name, get_parties_from_database,
                   get_votes_from_database)


def get_parties():
    print("Checking party names...")

    party_names = []
    id_sittings_list = get_id_sittings_list()

    for id in id_sittings_list:
        url = url_voting + id
        print(url)
        soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')

        url.strip(id)
        try:
            for link in soup.find_all('a'):
                link = link.get('href')
                if fnmatch.fnmatch(link, url_nr_sitting):
                    link = url_home_link + link
                    dataframe = pd.read_html(link, encoding='utf-8')[0]
                    partie = dataframe['Klub/Koło'].tolist()

                    for partia in partie:
                        if partia not in party_names:
                            party_names.append(partia)
                    break
        except Exception as e:
            print(f"Get parties: {e}")
            pass

    print('Downloaded')
    return party_names


def get_sittings():
    print("Checking sittings...")

    months = {
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

    id_sittings_list = get_id_sittings_list()
    try:
        dataframe = pd.read_html(url_sitting, encoding='utf-8')[0]
        dataframe = dataframe.drop(['Liczba głosowań', 'Unnamed: 3'], axis=1)
        dataframe = dataframe.rename(columns={'Nr pos. Sejmu': 'nr_posiedzenia', 'Data pos. Sejmu': 'data'})
        dataframe['nr_posiedzenia'] = dataframe['nr_posiedzenia'].fillna(method='ffill')

        date_list = dataframe['data'].tolist()
        new_date_list = []

        for date in date_list:
            date = date.strip(' r.')
            date = date.replace(' ', '-')
            for word, replacment in months.items(): date = date.replace(word, replacment)
            if len(date) == 9: date = '0' + date

            year = date[date.index('-') + 4:]
            month = date[date.index('-'):date.index('-') + 4].strip('-')
            day = date[:date.index('-')]
            date = year + '-' + month + '-' + day

            new_date_list.append(date)

        date_column = dataframe.columns[1]
        dataframe = dataframe.drop(date_column, axis=1)
        dataframe[date_column] = new_date_list
        dataframe['id'] = id_sittings_list
        dataframe = dataframe[['id', 'nr_posiedzenia', 'data']]

        # dataframe['nr_posiedzenia'] = dataframe['nr_posiedzenia'].astype(int)
        # dataframe['id'] = dataframe['id'].astype(int)
    except Exception as e:
        print(f"Get sittings: {e}")

    print('Pobrane')
    # return dataframe.to_csv('posiedzenia.csv', index=False)
    return dataframe


def get_votings():
    print("Checking votings...")

    column_names = ['id_posiedzenia', 'nr_glosowania', 'opis']
    joined_dataframe = pd.DataFrame(columns=column_names)

    id_posiedzen_list = get_id_sittings_list()

    for id in id_posiedzen_list:
        url_voting += id
        print(url_voting)

        try:
            dataframe = pd.read_html(url_voting, encoding='utf-8')[0]
            del dataframe['Godzina']
            dataframe = dataframe.rename(columns={'Nr': 'nr_glosowania', 'Temat': 'opis'})
            dataframe.insert(1, 'id_posiedzenia', id)
            joined_dataframe = pd.concat([joined_dataframe, pd.DataFrame.from_records(dataframe)])
            url_voting = url_voting.strip(id)
        except Exception as e:
            print(f"Get votings: {e}")
            continue

    # joined_dataframe['id_posiedzenia'] = joined_dataframe['id_posiedzenia'].astype(int)
    # joined_dataframe['nr_glosowania'] = joined_dataframe['nr_glosowania'].astype(int)

    print('Downloaded')
    # return joined_dataframe.to_csv('glosowanie.csv', index=False)
    return joined_dataframe


def get_deputies():
    print("Checking deputies...")

    id_deputies_list = get_id_deputies_list()

    column_names = ['id', 'imie', 'nazwisko']
    dataframe = pd.DataFrame(columns=column_names)
    names = []
    last_names = []

    try:
        soup = bs4.BeautifulSoup(requests.get(url_deputies, verify=True).text, 'html.parser')
        for link in soup.find_all('a'):
            link = link.get('href')
            if fnmatch.fnmatch(link, url_deputy):
                link = url_home_link2 + link
                print(link)
                soup = bs4.BeautifulSoup(requests.get(link, verify=True).text, 'html.parser')

                for full_name in soup.find_all('h1'):
                    full_name = full_name.get_text()
                    name = get_name(full_name)
                    names.append(name)
                    last_name = get_last_name(full_name)
                    last_names.append(last_name)

        dataframe['id'] = id_deputies_list
        dataframe['imie'] = names
        dataframe['nazwisko'] = last_names
    except Exception as e:
        print(f"Get deputies: {e}")
        pass

    print('Downloaded')
    # return dataframe.to_csv('poslowie.csv', index=False)
    return dataframe


def get_votes(id_deputy_from, id_deputy_to, id_sitting_from, id_sitting_to):
    print("Checking votes...")
    id_deputies_list = []
    id_sittings_list = []
    url_vote_deputy = 'https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=POSELGL&NrKadencji=9&Nrl='

    votes_database_table = get_votes_from_database()

    def check_deputies_party_id(url, name):
        found = False
        while found is False:
            try:
                soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')
                for link in soup.find_all('a'):
                    link = link.get('href')
                    if fnmatch.fnmatch(link, url_nr_sitting):
                        link = url_home_link + link

                        soup = bs4.BeautifulSoup(requests.get(link, verify=True).text, 'html.parser')

                        for party in soup.find_all('a'):
                            party = party.get('href')
                            if fnmatch.fnmatch(party, url_party_voting):
                                partia_link = url_home_link + party
                                print(partia_link)

                                found_party_name = party[party.index('&KodKlubu='):]
                                found_party_name = found_party_name[found_party_name.index('='):].strip('=')

                                dataframe = pd.read_html(partia_link, encoding='utf-8')[0]
                                dataframe_left = dataframe['Nazwisko i imię'].tolist()
                                dataframe_right = dataframe['Nazwisko i imię.1'].tolist()

                                deputies = dataframe_left + dataframe_right
                                for deputy in deputies:
                                    if deputy == name:
                                        found = True
                                        print(full_name + ' ' + found_party_name)
                                        break
                                pass
                            if found: break
                    if found: break
            except Exception as e:
                print(f"Check deputies party id: {e}")
                continue

        parties = get_parties_from_database()
        for index, row in parties.iterrows():
            if row['nazwa'] == found_party_name:
                return row['id']

    column_names = ['id_partia', 'id_posel', 'id_glosowania', 'glos', 'data_glosu']
    joined_dataframe = pd.DataFrame(columns=column_names)

    full_id_sittings_list = get_id_sittings_list()
    full_id_deputies_list = get_id_deputies_list()
    full_id_sittings_list.sort()
    full_id_deputies_list.sort()

    for i in full_id_sittings_list[full_id_sittings_list.index(id_sitting_from):full_id_sittings_list.index(id_sitting_to) + 1]:
        id_sittings_list.append(i)

    for j in full_id_deputies_list[full_id_deputies_list.index(id_deputy_from):full_id_deputies_list.index(id_deputy_to) + 1]:
        id_deputies_list.append(j)

    for id_deputy in id_deputies_list:
        url_vote_deputy += id_deputy

        for id_dep in id_sittings_list:
            counter = 0
            found_voting = False
            temp_sitting_link = '*IdDnia=' + id_dep

            while found_voting is False:
                try:
                    soup = bs4.BeautifulSoup(requests.get(url_vote_deputy, verify=True).text, 'html.parser')
                    print(url_vote_deputy)

                    for link in soup.find_all('a'):
                        link = link.get('href')
                        if fnmatch.fnmatch(link, temp_sitting_link):
                            found_voting = True
                            id_votes_list = []

                            temp_sitting_link = temp_sitting_link.strip(id_dep)
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

                            id_partii_posla = check_deputies_party_id(temp_link, new_full_name)

                            dataframe = pd.read_html(temp_link, encoding='utf-8')[0]
                            del dataframe['Godzina']
                            dataframe.insert(0, 'id_partia', id_partii_posla)
                            dataframe.insert(1, 'id_posel', id_deputy)
                            dataframe = dataframe.rename(columns={'Numer': 'nr_glosowania', 'Wynik': 'glos', 'Temat': 'opis'})
                            dataframe = dataframe[:-1]

                            for index1, row_glosowania in votes_database_table.iterrows():
                                if row_glosowania['id_posiedzenia'] == int(id_posiedzenia):
                                    id_vote = row_glosowania['id']
                                    description = row_glosowania['opis']
                                    vote_number = row_glosowania['nr_glosowania']

                                    for index2, row_dataframe in dataframe.iterrows():
                                        vote_number2 = row_dataframe['nr_glosowania']
                                        description2 = row_dataframe['opis']

                                        if vote_number == int(vote_number2) and description == description2:
                                            id_votes_list.append(id_vote)

                            del dataframe['opis']
                            del dataframe['nr_glosowania']
                            dataframe.insert(2, 'id_glosowania', id_votes_list)
                            dataframe.insert(3, 'data_glosu', date)
                            dataframe['data_glosu'] = dataframe['data_glosu'].fillna(method='ffill')

                            joined_dataframe = pd.concat([joined_dataframe, pd.DataFrame.from_records(dataframe)])

                    if found_voting is False:
                        print("Couldn\'t load voting, loading again")
                        counter += 1
                        if counter == 3:
                            print("Deputy was absent in this voting")
                            found_voting = True
                            break
                        continue
                except Exception as e:
                    print(f"Get votes: {e}")
                    continue

        url_vote_deputy = url_vote_deputy.strip(id_deputy)

    print('Downloaded')
    # joined_dataframe.to_csv('glosy.csv', index=False)
    return joined_dataframe
