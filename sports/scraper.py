import requests
import datetime
import urllib
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
from itertools import chain
from sports.models import Team

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

def fix_names(data):
    new_data = []
    for game in data:
        teams = game['scores']
        tag = str(game['id'][0])
        chopped = teams[0].split(' ')
        try:
            chopped.remove('')
        except ValueError:
            pass
        try:
            chopped.remove('')
        except ValueError:
            pass

        try:
            m = int(chopped[1])
            team_one = chopped[0]
        except ValueError:
            team_one = chopped[0] + ' ' + chopped[1]
            chopped.remove(chopped[1])
            chopped[0] = team_one
        try:
            m = int(chopped[3])
            team_two = chopped[2]

        except ValueError:
            team_two = chopped[2] + ' ' + chopped[3]
            chopped.remove(chopped[3])
            chopped[2] = team_two

        chopped.append(tag)
        new_data.append(chopped)
    return new_data

# data_list = (fix_names(nba_scores()))



def usable_data(data):
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
                info['winner_pts'] = round(((float(x[1]) - float(x[3])) * .5) + 3 + float(x[1]) * .08,3)
                info['loser'] = x[2]
                info['loser_pts'] = round(-((float(x[1]) - float(x[3])) * .5) -4 + float(x[1]) * .08,3)
                info['time'] = x[4]
                info['tag'] = x[5]
                if x[5] == 'IN':
                    info['tag'] = x[7]

                view_data.append(info)
            else:
                info = {}
                info['winner'] = x[2].replace('^', '')
                info['winner_pts'] = round(((float(x[3]) - float(x[1])) * .5) + 3 + float(x[1]) * .08,3)
                info['loser'] = x[0]
                info['loser_pts'] = round(-((float(x[3]) - float(x[1])) * .5) -4 + float(x[1]) * .08,3)
                info['time'] = x[4]
                info['tag'] = x[5]
                if x[5] == 'IN':
                    info['tag'] = x[7]
                view_data.append(info)
    return view_data
#
#print(usable_data(fix_names(nba_scores())))

# def duplicate_team(data):
#     for dictionary in data:
#         if dictionary['winner'] == 'LA':
#             check = requests.get(dictionary['tag'])
#             souper = BeautifulSoup(check.text, 'html.parser')
#             team = souper.find_all('span', title="LA")
#             for x in team:
#                 answer = x.text
#             if answer == "LAC":
#                 dictionary['winner'] == 'Clippers'
#                 return data
#             dictionary['winner'] == 'Lakers'
#             return data
#     return data
