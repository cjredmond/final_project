import requests
import datetime
import urllib
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
from itertools import chain

a='&nba_s_delay=120&nba_s_stamp=1117074359&nba_s_left1=Washington%20102%20%20%20^Philadelphia%20109%20(FINAL)&nba_s_right1_1=J.%20Wall%2027pts,%206ast,%204reb&nba_s_right1_2=S.%20Rodriguez%207pts,%2012ast,%204reb&nba_s_right1_count=2&nba_s_url1=http://www.espn.com/nba/boxscore?gameId=400899608&nba_s_left2=New%20Orleans%2082%20%20%20^Orlando%2089%20(FINAL)&nba_s_right2_1=T.%20Jones%2026pts,%202ast,%209reb&nba_s_right2_2=N.%20Vucevic%2010pts,%200ast,%2014reb&nba_s_right2_count=2&nba_s_url2=http://www.espn.com/nba/boxscore?gameId=400899609&nba_s_left3=Cleveland%2093%20%20%20^Indiana%20103%20(FINAL)&nba_s_right3_1=K.%20Love%2027pts,%201ast,%2016reb&nba_s_right3_2=P.%20George%2021pts,%205ast,%2011reb&nba_s_right3_3=M.%20Ellis%205%20blocks&nba_s_right3_count=3&nba_s_url3=http://www.espn.com/nba/boxscore?gameId=400899610&nba_s_left4=Dallas%2083%20%20%20^Boston%2090%20(FINAL)&nba_s_right4_1=H.%20Barnes%2028pts,%201ast,%202reb&nba_s_right4_2=I.%20Thomas%2030pts,%206ast,%204reb&nba_s_right4_3=W.%20Matthews%206-13%20three%20pointers&nba_s_right4_count=3&nba_s_url4=http://www.espn.com/nba/boxscore?gameId=400899611&nba_s_left5=Detroit%20102%20%20%20^New%20York%20105%20(FINAL)&nba_s_right5_1=J.%20Leuer%2017pts,%203ast,%209reb&nba_s_right5_2=K.%20Porzingis%2035pts,%203ast,%207reb&nba_s_right5_count=2&nba_s_url5=http://www.espn.com/nba/boxscore?gameId=400899612&nba_s_left6=Milwaukee%20100%20%20%20^Atlanta%20107%20(FINAL)&nba_s_right6_1=G.%20Antetokounmpo%2026pts,%207ast,%2015reb&nba_s_right6_2=P.%20Millsap%2021pts,%203ast,%208reb&nba_s_right6_count=2&nba_s_url6=http://www.espn.com/nba/boxscore?gameId=400899613&nba_s_left7=Houston%20103%20%20%20^Oklahoma%20City%20105%20(FINAL)&nba_s_right7_1=J.%20Harden%2013pts,%2013ast,%207reb&nba_s_right7_2=R.%20Westbrook%2030pts,%209ast,%207reb&nba_s_right7_3=V.%20Oladipo%205-7%20three%20pointers&nba_s_right7_count=3&nba_s_url7=http://www.espn.com/nba/boxscore?gameId=400899614&nba_s_left8=^Golden%20State%20127%20%20%20Toronto%20121%20(FINAL)&nba_s_right8_1=K.%20Durant%2030pts,%206ast,%209reb&nba_s_right8_2=D.%20DeRozan%2034pts,%204ast,%206reb&nba_s_right8_count=2&nba_s_url8=http://www.espn.com/nba/boxscore?gameId=400899615&nba_s_left9=Phoenix%20104%20%20%20^Denver%20120%20(FINAL)&nba_s_right9_1=B.%20Knight%2032pts,%204ast,%204reb&nba_s_right9_2=W.%20Chandler%2028pts,%205ast,%2011reb&nba_s_right9_count=2&nba_s_url9=http://www.espn.com/nba/boxscore?gameId=400899616&nba_s_left10=^Memphis%20111%20%20%20LA%20107%20(FINAL)&nba_s_right10_1=M.%20Conley%2030pts,%208ast,%205reb&nba_s_right10_2=B.%20Griffin%2025pts,%203ast,%208reb&nba_s_right10_3=J.%20Redick%207-12%20three%20pointers&nba_s_right10_count=3&nba_s_url10=http://www.espn.com/nba/boxscore?gameId=400899617&nba_s_left11=^San%20Antonio%20110%20%20%20Sacramento%20105%20(FINAL)&nba_s_right11_1=P.%20Gasol%2024pts,%202ast,%209reb&nba_s_right11_2=D.%20Cousins%2026pts,%206ast,%2017reb&nba_s_right11_count=2&nba_s_url11=http://www.espn.com/nba/boxscore?gameId=400899618&nba_s_count=11&nba_s_loaded=true'

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

data_list = [['Washington', '102', '^Philadelphia', '109', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899608'], ['New Orleans', '82', '^Orlando', '89', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899609'], ['Cleveland', '93', '^Indiana', '103', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899610'], ['Dallas', '83', '^Boston', '90', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899611'], ['Detroit', '102', '^New York', '105', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899612'], ['Milwaukee', '100', '^Atlanta', '107', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899613'], ['Houston', '103', '^Oklahoma City', '105', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899614'], ['^Golden State', '127', 'Toronto', '121', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899615'], ['Phoenix', '104', '^Denver', '120', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899616'], ['^Memphis', '111', 'LA', '107', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899617'], ['^San Antonio', '110', 'Sacramento', '105', '(FINAL)', 'http://www.espn.com/nba/boxscore?gameId=400899618']]


def usable_data(data):
    view_data = []
    for x in data:
        if not type(x[1]) is int:
            pass
        else:
            if int(x[1]) > int(x[3]):
                info = {}
                info['winner'] = x[0].replace('^', '')
                info['winner_pts'] = ((float(x[1]) - float(x[3])) * .5) + 3 + float(x[1]) * .08
                info['loser'] = x[2]
                info['loser_pts'] = -((float(x[1]) - float(x[3])) * .5) -4 + float(x[1]) * .08
                info['tag'] = x[5]
                info['time'] = x[4]
                view_data.append(info)
            else:
                info = {}
                info['winner'] = x[2].replace('^', '')
                info['winner_pts'] = ((float(x[3]) - float(x[1])) * .5) + 3 + float(x[1]) * .08
                info['loser'] = x[0]
                info['loser_pts'] = -((float(x[3]) - float(x[1])) * .5) -4 + float(x[1]) * .08
                info['tag'] = x[5]
                info['time'] = x[4]
                view_data.append(info)
    return view_data

# print(usable_data(fix_names(nba_scores())))
