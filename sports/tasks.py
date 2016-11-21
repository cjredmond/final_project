import time
from celery import Celery
import random
import datetime
import requests
from celery import shared_task
from sports.scraper import usable_data, fix_names, nba_scores
from sports.models import Score, Team, Squad

# app = Celery('tasks')
# app.conf.update(CELERY_ACCEPT_CONTENT = ['json'])
@shared_task
def cal():
    Packers = Team.objects.get(name='Packers')
    Score.objects.create(team=Packers,time=datetime.datetime.now(),pts=5,tag='http://www.google.com')
