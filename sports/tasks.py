import time
from celery import Celery
import random
import datetime
import requests
from celery import shared_task
from sports.scraper import usable_data, fix_names, nba_scores
from sports.nhl_scraper import nhl_scores, nhl_usable_data
from sports.nfl_scraper import nfl_scores, nfl_usable_data
from sports.models import Score, Team, Squad
from django.utils import timezone


@shared_task
def cal():
#     items_nba = usable_data(fix_names(nba_scores()))
#     for dictionary in items_nba:
#         if dictionary['winner'] == 'LA Lakers':
#             winner = Team.objects.get(name='Lakers')
#             loser = Team.objects.get(city=dictionary['loser'], sport='k')
#         elif dictionary['loser'] == 'LA Lakers':
#             winner = Team.objects.get(city=dictionary['winner'], sport='k')
#             loser = Team.objects.get(name='Lakers')
#         else:
#             winner = Team.objects.get(city=dictionary['winner'], sport='k')
#             loser = Team.objects.get(city=dictionary['loser'], sport='k')
#
#
#         if Score.objects.filter(tag=dictionary['tag']):
#             x = Score.objects.filter(tag=dictionary['tag'])
#             prev_winner = Score.objects.get(tag=dictionary['tag'], team=winner)
#             y = list(prev_winner.active_squad.all())
#             prev_winner.delete()
#             Score.objects.create(team=winner, pts=dictionary['winner_pts'],tag=dictionary['tag'], time=timezone.now())
#             #squads = list(Squad.objects.filter(roster__name=winner.name))
#             current = Score.objects.get(team=winner,tag=dictionary['tag'])
#             current.active_squad.add(*y)
#             current.save()
#
#             prev_loser = Score.objects.get(tag=dictionary['tag'], team=loser)
#             y = list(prev_loser.active_squad.all())
#             prev_loser.delete()
#             Score.objects.create(team=loser, pts=dictionary['loser_pts'],tag=dictionary['tag'], time=timezone.now())
#             current = Score.objects.get(team=loser,tag=dictionary['tag'])
#             current.active_squad.add(*y)
#             current.save()
#         else:
#             Score.objects.filter(tag=dictionary['tag']).delete()
#             Score.objects.create(team=winner, pts=dictionary['winner_pts'],tag=dictionary['tag'], time=timezone.now())
#             squads = list(Squad.objects.filter(roster__name=winner.name))
#             current = Score.objects.get(team=winner,tag=dictionary['tag'])
#             current.active_squad.add(*squads)
#             current.save()
#
#             Score.objects.create(team=loser, pts=dictionary['loser_pts'],tag=dictionary['tag'], time=timezone.now())
#             squads = list(Squad.objects.filter(roster__name=loser.name))
#             current = Score.objects.get(team=loser,tag=dictionary['tag'])
#             current.active_squad.add(*squads)
#             current.save()
#
# ########## HOCKEY ##########
#
#     items_nhl = nhl_usable_data(fix_names(nhl_scores()))
#     for dictionary in items_nhl:
#         winner = Team.objects.get(city=dictionary['winner'], sport='h')
#         loser = Team.objects.get(city=dictionary['loser'], sport='h')
#         #Score.objects.filter(tag=dictionary['tag']).delete()
#
#         x = Score.objects.filter(tag=dictionary['tag'])
#         if x:
#             prev_winner = Score.objects.get(tag=dictionary['tag'], team=winner)
#             y = list(prev_winner.active_squad.all())
#             prev_winner.delete()
#             Score.objects.create(team=winner, pts=dictionary['winner_pts'],tag=dictionary['tag'], time=timezone.now())
#             #squads = list(Squad.objects.filter(roster__name=winner.name))
#             current = Score.objects.get(team=winner,tag=dictionary['tag'])
#             current.active_squad.add(*y)
#             current.save()
#
#             prev_loser = Score.objects.get(tag=dictionary['tag'], team=loser)
#             y = list(prev_loser.active_squad.all())
#             prev_loser.delete()
#             Score.objects.create(team=loser, pts=dictionary['loser_pts'],tag=dictionary['tag'], time=timezone.now())
#             current = Score.objects.get(team=loser,tag=dictionary['tag'])
#             current.active_squad.add(*y)
#             current.save()
#
#         else:
#             Score.objects.filter(tag=dictionary['tag']).delete()
#             Score.objects.create(team=winner, pts=dictionary['winner_pts'],tag=dictionary['tag'], time=timezone.now())
#             squads = list(Squad.objects.filter(roster__name=winner.name))
#             current = Score.objects.get(team=winner,tag=dictionary['tag'])
#             current.active_squad.add(*squads)
#             current.save()
#
#             Score.objects.create(team=loser, pts=dictionary['loser_pts'],tag=dictionary['tag'], time=timezone.now())
#             squads = list(Squad.objects.filter(roster__name=loser.name))
#             current = Score.objects.get(team=loser,tag=dictionary['tag'])
#             current.active_squad.add(*squads)
#             current.save()
#### FOOTBALL ######
    items_nfl = nfl_usable_data(fix_names(nfl_scores()))
    for dictionary in items_nfl:
        winner = Team.objects.get(city=dictionary['winner'], sport='f')
        loser = Team.objects.get(city=dictionary['loser'], sport='f')
        #Score.objects.filter(tag=dictionary['tag']).delete()

        x = Score.objects.filter(tag=dictionary['tag'])
        if x:
            prev_winner = Score.objects.get(tag=dictionary['tag'], team=winner)
            y = list(prev_winner.active_squad.all())
            prev_winner.delete()
            Score.objects.create(team=winner, pts=dictionary['winner_pts'],tag=dictionary['tag'], time=timezone.now())
            #squads = list(Squad.objects.filter(roster__name=winner.name))
            current = Score.objects.get(team=winner,tag=dictionary['tag'])
            current.active_squad.add(*y)
            current.save()

            prev_loser = Score.objects.get(tag=dictionary['tag'], team=loser)
            y = list(prev_loser.active_squad.all())
            prev_loser.delete()
            Score.objects.create(team=loser, pts=dictionary['loser_pts'],tag=dictionary['tag'], time=timezone.now())
            current = Score.objects.get(team=loser,tag=dictionary['tag'])
            current.active_squad.add(*y)
            current.save()

        else:
            Score.objects.filter(tag=dictionary['tag']).delete()
            Score.objects.create(team=winner, pts=dictionary['winner_pts'],tag=dictionary['tag'], time=timezone.now())
            squads = list(Squad.objects.filter(roster__name=winner.name))
            current = Score.objects.get(team=winner,tag=dictionary['tag'])
            current.active_squad.add(*squads)
            current.save()

            Score.objects.create(team=loser, pts=dictionary['loser_pts'],tag=dictionary['tag'], time=timezone.now())
            squads = list(Squad.objects.filter(roster__name=loser.name))
            current = Score.objects.get(team=loser,tag=dictionary['tag'])
            current.active_squad.add(*squads)
            current.save()
