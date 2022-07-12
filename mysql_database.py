import mysql.connector
# import html_scraper

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "kamil123",
    database = "testdatabase"
)

mycursor = db.cursor()

sql_partie = '''CREATE TABLE partie (
                id_partia int PRIMARY KEY AUTO_INCREMENT, 
                nazwa VARCHAR(20) NOT NULL)'''

sql_poslowie = '''CREATE TABLE poslowie (
                id_posel int PRIMARY KEY AUTO_INCREMENT, 
                id_partia int, FOREIGN KEY (id_partia) REFERENCES partie(id_partia), 
                imie VARCHAR(30) NOT NULL, nazwisko VARCHAR(30) NOT NULL)'''


# sql = "INSERT INTO partie(nazwa) VALUES (%s)",nazwa
# mysql.mycursor.execute(sql)
# mysql.db.commit()

# mycursor.execute(sql_poslowie)

# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#     print(x)