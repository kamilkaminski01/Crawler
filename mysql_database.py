import mysql.connector

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
                imie VARCHAR(30) NOT NULL, 
                nazwisko VARCHAR(30) NOT NULL)'''

sql_posiedzenia = '''CREATE TABLE posiedzenia (
                    id_posiedzenia int PRIMARY KEY AUTO_INCREMENT,
                    nr_posiedzenia int NOT NULL,
                    data DATE NOT NULL)'''


# mycursor.execute(sql_partie)
# mycursor.execute(sql_poslowie)
# mycursor.execute(sql_posiedzenia)

mycursor.execute(sql_poslowie)

db.commit()

# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#     print(x)