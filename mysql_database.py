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
# posiedzenia_dataframe = get_posiedzenia()
# glosowania_dataframe = get_glosowania()
# poslowie_dataframe = get_poslowie()


create_table_partie = '''CREATE TABLE partie (id_partia int PRIMARY KEY AUTO_INCREMENT, nazwa VARCHAR(20) NOT NULL)'''
create_table_poslowie = '''CREATE TABLE poslowie (id_posel int PRIMARY KEY, imie VARCHAR(30) NOT NULL, nazwisko VARCHAR(30) NOT NULL)'''
create_table_posiedzenia = '''CREATE TABLE posiedzenia (id_posiedzenia int PRIMARY KEY, nr_posiedzenia int NOT NULL, data DATE NOT NULL)'''
create_table_glosowania = '''CREATE TABLE glosowania (id_glosowania int PRIMARY KEY AUTO_INCREMENT, id_posiedzenia int NOT NULL, 
                            nr_glosowania int NOT NULL,opis VARCHAR(2000) NOT NULL, FOREIGN KEY(id_posiedzenia) REFERENCES posiedzenia(id_posiedzenia))'''


# Funkcja do sprawdzenia czy posiedzenie istnieje w bazie danych na podstawie id_posiedzenia
def posiedzenie_exists(cursor, id_posiedzenia):
    query = ('''SELECT id_posiedzenia FROM posiedzenia WHERE id_posiedzenia = %s''')
    cursor.execute(query, (id_posiedzenia,))
    return cursor.fetchone() is not None

# Funkcja do wstawienia danych o posiedzeniu
def insert_posiedzenia(cursor, id_posiedzenia, nr_posiedzenia, data):
    insert_into_posiedzenia = ('''INSERT INTO posiedzenia (id_posiedzenia, nr_posiedzenia, data) VALUES (%s,%s,%s)''')
    row_to_insert = (id_posiedzenia, nr_posiedzenia, data)
    cursor.execute(insert_into_posiedzenia, row_to_insert)

# Wstawianie posiedzeń do bazy danych
def execute_posiedzenia():
    for index, row in posiedzenia_dataframe.iterrows():
        # Jeśli posiedzenie istnieje w bazie danych, przejście dalej
        if posiedzenie_exists(cursor, row['id_posiedzenia']): pass
        # Jeśli posiedzenie nie istnieje w bazie danych, dodanie rzędu
        else: insert_posiedzenia(cursor, row['id_posiedzenia'], row['nr_posiedzenia'], row['data'])

# Funkcja do sprawdzenia czy istnieje głosowanie w bazie danych na podstawie opisu
def glosowanie_exists(cursor, nr_glosowania, opis):
    query = ('''SELECT nr_glosowania, opis FROM glosowania WHERE nr_glosowania = %s AND opis = %s''')
    row_to_insert = (nr_glosowania, opis)
    cursor.execute(query, row_to_insert)
    return cursor.fetchone() is not None

# Funkcja do wstawienia danych o głosowaniu
def insert_glosowanie(cursor, id_posiedzenia, nr_glosowania, opis):
    insert_into_glosowania = ('''INSERT INTO glosowania SET id_posiedzenia = (SELECT id_posiedzenia FROM posiedzenia WHERE id_posiedzenia = %s), nr_glosowania = %s, opis = %s''')
    row_to_insert = (id_posiedzenia, nr_glosowania, opis)
    cursor.execute(insert_into_glosowania, row_to_insert)

# Wstawianie głosowań do bazy danych
def execute_glosowania():
    for index, row in glosowania_dataframe.iterrows():
        if glosowanie_exists(cursor, row['nr_glosowania'], row['opis']): pass
        else: insert_glosowanie(cursor, row['id_posiedzenia'], row['nr_glosowania'], row['opis'])

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

# Funkcja do sprawdzenia czy posel istnieje w bazie danych na podstawie ID
def posel_exists(cursor, id_posel):
    query = ('''SELECT id_posel from poslowie WHERE id_posel = %s''')
    cursor.execute(query, (id_posel,))
    return cursor.fetchone() is not None

# Funkcja do wstawienia danych o pośle
def insert_posel(cursor, id_posel, imie, nazwisko):
    insert_into_poslowie = ('''INSERT INTO poslowie (id_posel, imie, nazwisko) VALUES (%s,%s,%s)''')
    row_to_insert = (id_posel, imie, nazwisko)
    cursor.execute(insert_into_poslowie, row_to_insert)

def execute_poslowie():
    for index, row in poslowie_dataframe.iterrows():
        # Jeśli poseł istnieje w bazie danych, przejście dalej
        if posel_exists(cursor, row['id_posel']): pass
        # Jeśłi poseł nie istnieje w bazie danych, dodanie rzędu
        else: insert_posel(cursor, row['id_posel'], row['imie'], row['nazwisko'])

# execute_partie()
# execute_posiedzenia()
# execute_glosowania()
# execute_poslowie()

# cursor.execute(create_table_partie)
# cursor.execute(create_table_poslowie)
# cursor.execute(create_table_posiedzenia)
# cursor.execute(create_table_glosowania)

# db.commit()