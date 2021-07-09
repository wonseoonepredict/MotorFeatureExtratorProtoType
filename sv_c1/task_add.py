from celery import Celery
from sv_c1.celery_main import celery_app

@celery_app.task
def add(x,y):
    return x + y




