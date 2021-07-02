from celery import Celery
from sv_c1.main import app
import os

def process(msg:str):
    process_execute.apply_async((msg,))

@app.task
def process_execute(msg):
    print(os.getpid(), msg)
