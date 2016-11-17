import requests
import datetime
import urllib
from bs4 import BeautifulSoup
from urllib.parse import parse_qs

base_url = 'http://www.espnfc.us/english-premier-league/23/scores'
data = requests.get(base_url)
souper = BeautifulSoup(data.text, 'html.parser')
tags = souper.find_all('a')
