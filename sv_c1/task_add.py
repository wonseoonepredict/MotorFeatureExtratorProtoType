from celery import Celery
from .main import app

@app.task
def add(x,y):
    return x + y




