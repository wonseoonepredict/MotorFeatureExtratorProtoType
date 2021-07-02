import time
import signal

from celery import Celery
from celery.signals import celeryd_init, worker_shutting_down
from celery.utils.dispatch import Signal

CELERY_BROKER='redis://10.10.70.140:6379/0'
CELERY_RESULT='redis://10.10.70.140:6379/0'

from lib.event.event_listener import start as listener_start
from lib.event.event_listener import terminate as listener_end

signals=['SIGTERM', 'SIGINT', 'SIGSEGV']

print('-- start celery --')
app = Celery('tasks', broker=CELERY_BROKER, backend=CELERY_RESULT)


from .task_process import process as task_process
from lib.event.event_listener import set_process_cb
print('-- set task_process_cb --')
set_process_cb(task_process)


@celeryd_init.connect
def init_signals(*args, **kwargs):
    print('init_signals')
    add_signal_handler()


"""
{'signal': <Signal: worker_shutting_down providing_args=set()>, 'sender': 'celery@OnePredictui-MacBookPro.local', 'sig': 'SIGINT', 'how': 'Warm', 'exitcode': 1}
"""


## celery의 종료 시그널을 intercept하여 listener를 종료합니다.
@worker_shutting_down.connect
def fint_server(*args, **kwargs):
    if kwargs['sig'] in signals:
        print('\\----------------------------\\')
        print('\\ Server will be terminated. \\')
        print('\\----------------------------\\')
        listener_end()
        time.sleep(3)
    

print('-- start listener --')
if listener_start():
    print('Success to create listener...')
else:
    print('Fail to create listner...')
    exit()
