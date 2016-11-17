import requests
import datetime
import urllib
from bs4 import BeautifulSoup
from urllib.parse import parse_qs


def nba_scores():
    base_url_nba = 'http://www.espn.com/nba/bottomline/scores'
    data = requests.get(base_url_nba)
    x = urllib.parse.unquote(data.text)
    d = "nba_s_left"
    game = [d+e for e in data.text.split(d)]
    game_scores = []
    for g in game[1:]:
        current_score = {}
        for k,v in parse_qs (g).items():
            if k.startswith('nba_s_left'):
                current_score['scores'] = v
            if k.startswith('nba_s_url'):
                current_score['id'] = v
        game_scores.append(current_score)
    return game_scores
