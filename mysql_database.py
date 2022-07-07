import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "kamil123",
    database = "testdatabase"
)

mycursor = db.cursor()

# mycursor.execute("CREATE TABLE person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")
# mycursor.execute("INSERT INTO person (name, age) VALUES (%s,%s)",("Joe",22))
# mycursor.execute("DELETE FROM person WHERE personID = 2")
db.commit()
mycursor.execute("SELECT * FROM person")

for x in mycursor:
    print(x)