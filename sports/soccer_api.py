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

premier_league = []
for x in score_content:
    #print(x.find_all('div', class_='team-score'))

    z = x.find_all('img')
    if z:
        info = {}
        #print(a)
        #print(x.find_all('div', class_='team-score')[0])
        info['time'] = x.find_all('span', class_='time')
        info['home_score'] = x.find_all('div', class_='team-score')[0]
        info['away_score'] = x.find_all('div', class_='team-score')[1]


    for i,a in enumerate(z):
        if i == 0:
            info['home'] = a.attrs['alt']
        else:
            info['away'] = a.attrs['alt']
            premier_league.append(info)


        #print(a.attrs['alt'])
print(premier_league[0])
