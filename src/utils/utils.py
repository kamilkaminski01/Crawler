import fnmatch
from typing import Optional

import bs4  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore

from utils.consts import db, url_deputies, url_deputy, url_sitting


def load_site(url: str) -> Optional[bs4.BeautifulSoup]:
    soup = None
    loaded = False
    while loaded is False:
        try:
            soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, "html.parser")
            loaded = True
        except Exception as e:
            print(f"Loading site failed: {e}")
            continue
    return soup


def load_dataframe_with_pandas(url: str) -> Optional[pd.DataFrame]:
    dataframe = None
    loaded = False
    while loaded is False:
        try:
            dataframe = pd.read_html(url, encoding="utf-8")[0]
            loaded = True
        except Exception as e:
            print(f"Loading dataframe failed: {e}")
            if len(e.args) > 0 and e.args[0] == "No tables found":
                loaded = True
            else:
                continue
    return dataframe


def get_id_sittings_list() -> list:
    id_sittings_list = []
    try:
        soup: bs4.BeautifulSoup = load_site(url_sitting)
        for link in soup.find_all("a"):
            link = link.get("href")
            if fnmatch.fnmatch(link, "*IdDnia=*"):
                link = link[link.index("IdDnia=") :].strip("IdDnia=")
                id_sittings_list.append(link)
    except Exception as e:
        print(f"Get id sittings list: {e}")
    return id_sittings_list


def get_id_deputies_list() -> list:
    id_deputies_list = []
    try:
        soup: bs4.BeautifulSoup = load_site(url_deputies)
        for link in soup.find_all("a"):
            link = link.get("href")
            if fnmatch.fnmatch(link, url_deputy):
                id = link[link.index("id=") : link.index("&")].strip("id=")
                id_deputies_list.append(id)
    except Exception as e:
        print(f"Get id deputies list: {e}")
    return id_deputies_list


def get_name(full_name) -> str:
    result = None
    while result is None:
        try:
            if full_name.count(" ") == 1:
                return full_name.split(" ")[0]
            elif full_name.count(" ") == 2:
                return " ".join(full_name.split(" ", 2)[:2])
            elif full_name.count(" ") == 3:
                return full_name.split(" ")[0]
        except Exception as e:
            print(f"Get name: {e}")
            continue


def get_last_name(full_name) -> str:
    result = None
    while result is None:
        try:
            if full_name.count(" ") == 1:
                return full_name.split(" ")[1]
            elif full_name.count(" ") == 2:
                return full_name.split(" ")[2]
            elif full_name.count(" ") == 3:
                return " ".join(full_name.split(" ")[1:])
        except Exception as e:
            print(f"Get last name: {e}")
            continue


def get_votes_from_database():
    sql = """SELECT * FROM glosowania"""
    return pd.read_sql(sql, db)


def get_parties_from_database():
    sql = """SELECT * FROM partie"""
    return pd.read_sql(sql, db)
