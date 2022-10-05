from urls_variables import cursor, db

create_table_partie = '''CREATE TABLE partie
                        (id int PRIMARY KEY AUTO_INCREMENT,
                        nazwa VARCHAR(50) NOT NULL)'''

create_table_poslowie = '''CREATE TABLE poslowie
                            (id int PRIMARY KEY,
                            imie VARCHAR(30) NOT NULL,
                            nazwisko VARCHAR(30) NOT NULL)'''

create_table_posiedzenia = '''CREATE TABLE posiedzenia
                                (id int PRIMARY KEY,
                                nr_posiedzenia int NOT NULL,
                                data DATE NOT NULL)'''

create_table_glosowania = '''CREATE TABLE glosowania
                            (id int PRIMARY KEY AUTO_INCREMENT,
                            id_posiedzenia int NOT NULL,
                            nr_glosowania int NOT NULL,
                            opis VARCHAR(2000) NOT NULL,
                            FOREIGN KEY(id_posiedzenia) REFERENCES posiedzenia(id))'''

create_table_glosy = '''CREATE TABLE glosy
                        (id int PRIMARY KEY AUTO_INCREMENT,
                        id_partia int NOT NULL,
                        id_posel int NOT NULL,
                        id_glosowania int NOT NULL,
                        glos ENUM('Za', 'Przeciw', 'Wstrzymał się', 'Nie głosował', 'Głos oddany na listę') NOT NULL,
                        data_glosu DATE NOT NULL,
                        FOREIGN KEY(id_partia) REFERENCES partie(id),
                        FOREIGN KEY(id_posel) REFERENCES poslowie(id),
                        FOREIGN KEY(id_glosowania) REFERENCES glosowania(id))'''

cursor.execute(create_table_partie)
cursor.execute(create_table_poslowie)
cursor.execute(create_table_posiedzenia)
cursor.execute(create_table_glosowania)
cursor.execute(create_table_glosy)
db.commit()
