import time
from celery import Celery
import random
import datetime
import requests

app = Celery('tasks')
@app.task
def cal():
    now = datetime.datetime.now()
    print(now)
    time.sleep(random.randint(0,5))
    print(now)
