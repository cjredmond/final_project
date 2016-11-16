import requests
from bs4 import BeautifulSoup
base_url_nfl = 'http://www.espn.com/nfl/bottomline/scores'
data = requests.get(base_url_nfl)
souper = BeautifulSoup(data.text, 'html.parser')
