import requests
import datetime
import urllib
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
from sports.scraper import fix_names



def nfl_scores():
    url = 'http://www.espn.com/nfl/bottomline/scores'
    data = requests.get(url)
    x = urllib.parse.unquote(data.text)
    d = "nfl_s_left"
    game = [d+e for e in data.text.split(d)]
    game_scores = []
    for g in game[1:]:
        current_score = {}
        for k,v in parse_qs (g).items():
            if k.startswith('nfl_s_left'):
                current_score['scores'] = v
            if k.startswith('nfl_s_url'):
                current_score['id'] = v
        game_scores.append(current_score)
    return game_scores

def nfl_usable_data(data):
    view_data = []
    for x in data:
        try:
            int(x[1])
        except:
            ValueError
            pass
        else:
            if int(x[1]) > int(x[3]):
                info = {}
                info['winner'] = x[0].replace('^', '')
                info['winner_pts'] = round((float(x[1]) - float(x[3]))*2 + 2 + float(x[1]) * .8,3)
                info['loser'] = x[2]
                info['loser_pts'] = round((float(x[3]) - float(x[1])) - 2 + float(x[1]) * .8,3)
                info['time'] = x[4]
                info['tag'] = x[5]
                if x[5] == 'IN':
                    info['tag'] = x[7]
                if x[5] =='OF':
                    info['tag'] = x[7]

                view_data.append(info)
            else:
                info = {}
                info['winner'] = x[2].replace('^', '')
                info['winner_pts'] = round((float(x[3]) - float(x[1]))*2 + 2 + float(x[1]) * .8,3)
                info['loser'] = x[0]
                info['loser_pts'] = round((float(x[1]) - float(x[3])) -2 + float(x[1]) * .8,3)
                info['time'] = x[4]
                info['tag'] = x[5]
                if x[5] == 'IN':
                    info['tag'] = x[7]
                if x[5] =='OF':
                    info['tag'] = x[7]
                view_data.append(info)
    return view_data
# x = nfl_usable_data(fix_names(nfl_scores()))
# print(x)
