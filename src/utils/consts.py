import mysql.connector

# import pymysql

url_nr_sitting = "*agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia=*"
url_home_link = "https://www.sejm.gov.pl/Sejm9.nsf/"
url_home_link2 = "https://www.sejm.gov.pl"
url_party_voting = "*agent.xsp?symbol=klubglos&IdGlosowania=*"
url_sitting = "https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=posglos&NrKadencji=9"
url_voting = "https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=listaglos&IdDnia="
url_deputies = "https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=C"
url_deputy = "*posel.xsp?id=*"
url_vote_deputy = (
    "https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=POSELGL&NrKadencji=9&Nrl="
)


# Połączenie do lokalnej bazy danych MySQL
db = mysql.connector.connect(
    host="localhost", user="root", passwd="kamil123", database="testdatabase"
)

# Połączenie do bazy danych MySQL w AWS
"""
db = pymysql.connect(
    host="gov-crawler.ces9mzhykkcv.eu-central-1.rds.amazonaws.com",
    user="admin",
    password="i11ABnAs3KIp7IrwgOhkYQlPF9E3hxH1",
    database="gov-crawler"
)
"""
cursor = db.cursor()
