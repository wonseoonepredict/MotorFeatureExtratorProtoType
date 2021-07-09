from celery import Celery
import os

def process(msg:str):
    process_execute.apply_async((msg,))

from sv_c1.celery_main import celery_app

@celery_app.task
def process_execute(msg)->bool:
    print(os.getpid(), msg)
    return True
