import pandas as pd
import bs4
import requests

url = 'https://sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=klubglos&IdGlosowania=53744&KodKlubu=PiS'
# soup = bs4.BeautifulSoup(requests.get(url, verify=True).text, 'html.parser')
# table = soup.find_all('table')

df = pd.read_html(url)

print(df[0])