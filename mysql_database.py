import mysql.connector
import pandas as pd
from html_scraper import *

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "kamil123",
    database = "testdatabase"
)

cursor = db.cursor()
posiedzenia_dataframe = get_posiedzenia()
# glosowania_dataframe = get_glosowania()


create_table_partie = '''CREATE TABLE partie (id_partia int PRIMARY KEY AUTO_INCREMENT, nazwa VARCHAR(20) NOT NULL)'''
create_table_poslowie = '''CREATE TABLE poslowie (id_posel int PRIMARY KEY AUTO_INCREMENT, imie VARCHAR(30) NOT NULL, nazwisko VARCHAR(30) NOT NULL)'''
create_table_posiedzenia = '''CREATE TABLE posiedzenia (id_posiedzenia int PRIMARY KEY, nr_posiedzenia int NOT NULL, data DATE NOT NULL)'''
create_table_glosowania = '''CREATE TABLE glosowania (id_glosowania int PRIMARY KEY AUTO_INCREMENT, id_posiedzenia int NOT NULL, opis VARCHAR(2000) NOT NULL,
                            FOREIGN KEY(id_posiedzenia) REFERENCES posiedzenia(id_posiedzenia))'''


# Funkcja do sprawdzenia czy posiedzenie istnieje w bazie danych na podstawie id_posiedzenia
def posiedzenie_exists(cursor, id_posiedzenia):
    query = ('''SELECT id_posiedzenia FROM posiedzenia WHERE id_posiedzenia = %s''')
    cursor.execute(query, (id_posiedzenia,))
    return cursor.fetchone() is not None

# Funkcja do wstawienia danych o posiedzeniu
def insert_posiedzenia(cursor, id_posiedzenia, nr_posiedzenia, data):
    insert_into_posiedzenia = ('''INSERT INTO posiedzenia (id_posiedzenia, nr_posiedzenia, data) VALUES (%d,%d,%s)''')
    row_to_insert = (id_posiedzenia, nr_posiedzenia, data)
    cursor.execute(insert_into_posiedzenia, row_to_insert)

# Wstawianie posiedzeń do bazy danych
def execute_posiedzenia():
    for index, row in posiedzenia_dataframe.iterrows():
        # Jeśli posiedzenie istnieje w bazie danych, przejście dalej
        if posiedzenie_exists(cursor, row['id_posiedzenia']): pass
        # Jeśli posiedzenie nie istnieje w bazie danych, dodanie rzędu
        else: insert_posiedzenia(cursor, row['id_posiedzenia'], row['nr_posiedzenia'], row['data'])

# Funkcja do sprawdzenia czy istnieje głosowanie w bazie danych na podstawie id_glosowania
def glosowanie_exists(cursor, id_glosowania):
    query = ('''SELECT id_glosowania FROM glosowania WHERE id_glosowania = %s''')
    cursor.execute(query, (id_glosowania,))
    return cursor.fetchone() is not None

# Funkcja do wstawienia danych o głosowaniu
def insert_glosowanie(cursor, id_glosowania, id_posiedzenia, nr_glosowania, opis):
    insert_into_glosowania = ('''INSERT INTO glosowania (id_glosowania, id_posiedzenia, nr_glosowania, opis) VALUES (%d,%d,%d,%s)''')
    row_to_insert = (id_glosowania, id_posiedzenia, nr_glosowania, opis)
    cursor.execute(insert_into_glosowania, row_to_insert)

# Wstawianie głosowań do bazy danych
def execute_glosowania():
    for index, row in glosowania_dataframe.itterows():
        if glosowanie_exists(cursor, row['id_glosowania']): pass
        else: insert_glosowanie(cursor, row['id_glosowania'], row['id_posiedzenia'], row['nr_glosowania'], row['opis'])


# Funkcja do sprawdzenia czy partia istnieje w bazie danych na podstawie nazwy
def partia_exists(cursor, nazwa):
    query = ('''SELECT nazwa FROM partie WHERE nazwa = %s''')
    cursor.execute(query, (nazwa,))
    return cursor.fetchone() is not None

# Funkcja do wstawienia danych o partii
def insert_partie(cursor, partia):
    insert_into_partie = ('''INSERT INTO partie (nazwa) VALUES (%s)''')
    cursor.execute(insert_into_partie, (partia,))

# Wstawienie partii do bazy danych
def execute_partie():
    # Pętla korzysta z listy partii w pliku html_scraper
    for partia in partie:
        # Jeśli partia istnieje w bazie danych, przejście dalej
        if partia_exists(cursor, partia): pass
        # Jeśli partia nie istnieje w bazie danych, dodanie rzędu
        else: insert_partie(cursor, partia)




# execute_posiedzenia()
# execute_partie()

# cursor.execute(create_table_partie)
# cursor.execute(create_table_poslowie)
# cursor.execute(create_table_posiedzenia)
cursor.execute(create_table_glosowania)

db.commit()

# cursor.execute("SELECT * FROM partie")
# for x in cursor:
#     print(x)