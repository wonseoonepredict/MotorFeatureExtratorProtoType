import time
import signal

from celery import Celery
from sv_c1.celery_main import celery_app

from lib.event.event_listener import start as listener_start


print('-- start listener --')
if listener_start():
    print('Success to create listener...')
else:
    print('Fail to create listner...')
    exit()

