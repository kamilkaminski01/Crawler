import fnmatch

import bs4
import pandas as pd
import requests  # type: ignore

from urls_variables import db, url_deputies, url_deputy, url_sitting


def load_site(url):
    loaded = False
    while loaded is False:
        try:
            soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')
            loaded = True
            return soup
        except Exception as e:
            print(f"Loading site failed: {e}")
            continue


def load_dataframe_with_pandas(url):
    loaded = False
    while loaded is False:
        try:
            dataframe = pd.read_html(url, encoding='utf-8')[0]
            loaded = True
            return dataframe
        except Exception as e:
            print(f"Loading dataframe failed: {e}")
            if len(e.args) > 0 and e.args[0] == "No tables found":
                loaded = True
            else:
                continue


def get_id_sittings_list():
    id_sittings_list = []
    try:
        soup = bs4.BeautifulSoup(requests.get(url_sitting, verify=True).text, 'html.parser')
        for link in soup.find_all('a'):
            link = link.get('href')
            if fnmatch.fnmatch(link, '*IdDnia=*'):
                link = link[link.index('IdDnia='):].strip('IdDnia=')
                id_sittings_list.append(link)
        return id_sittings_list
    except Exception as e:
        print(f"Get id sittings list: {e}")


def get_id_deputies_list():
    id_deputies_list = []
    try:
        soup = bs4.BeautifulSoup(requests.get(url_deputies, verify=True).text, 'html.parser')
        for link in soup.find_all('a'):
            link = link.get('href')
            if fnmatch.fnmatch(link, url_deputy):
                id = link[link.index('id='):link.index('&')].strip('id=')
                id_deputies_list.append(id)
        return id_deputies_list
    except Exception as e:
        print(f"Get id deputies list: {e}")


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
            print(f"Get name: {e}")
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
            print(f"Get last name: {e}")
            continue


def get_votes_from_database():
    sql = '''SELECT * FROM glosowania'''
    return pd.read_sql(sql, db)


def get_parties_from_database():
    sql = '''SELECT * FROM partie'''
    return pd.read_sql(sql, db)
