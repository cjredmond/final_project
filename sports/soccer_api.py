import requests
import datetime
import urllib
from bs4 import BeautifulSoup
from urllib.parse import parse_qs

base_url = 'http://www.espnfc.us/english-premier-league/23/scores'
data = requests.get(base_url)
souper = BeautifulSoup(data.text, 'html.parser')

score_content = souper.find_all('div', class_="score-content")

y = souper.find_all('div', class_='team-name')


for x in score_content:
    #print(x.find_all('div', class_='team-score'))

    z = x.find_all('img')
    if z:
        a = x.find_all('span', class_='time')
        print(a)
        print(x.find_all('div', class_='team-score'))
    for a in z:
        print(a.attrs['alt'])
