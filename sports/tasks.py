import time
from celery import Celery
import random
import datetime
import requests
from celery import shared_task
from sports.scraper import usable_data, fix_names, nba_scores

# app = Celery('tasks')
# app.conf.update(CELERY_ACCEPT_CONTENT = ['json'])
@shared_task
def cal():
    x = usable_data(fix_names(nba_scores()))
    print('Hi')
    return x
