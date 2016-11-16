import requests
import datetime
from bs4 import BeautifulSoup
base_url_nfl = 'http://www.espn.com/nfl/bottomline/scores'
data = requests.get(base_url_nfl)
souper_nfl = BeautifulSoup(data.text, 'html.parser')
string_soup_nfl = str(souper_nfl)
split_soup_nfl = string_soup_nfl.split('http://sports.espn.go.com/nfl/preview?gameId=')
for x in split_soup_nfl:
    # print(x)
    # print('\n')
    pass

base_url_nba = 'http://www.espn.com/nba/bottomline/scores'
data = requests.get(base_url_nba)
souper_nba = BeautifulSoup(data.text, 'html.parser')
string_soup_nba = str(souper_nba)

split_soup_nba = string_soup_nba.split('gameId')
for x in split_soup_nba:
    print(x)
    print('\n')
