import json
import time as pytime
import sys
import threading
import signal

from lib.redis.redisqueue import RedisQueue

handler=None

q = RedisQueue('my-queue', host='localhost', port=6379, db=0)

go = True
task_process=None


def terminate():
    global go
    print('queue_listener will be terminated.')
    if handler is not None:
        go = False
        pytime.sleep(2)
        handler.join()


def set_process_cb(process_cb):
    global task_process
    print(process_cb)
    task_process = process_cb


def queue_listener():
    print('queue_listener is created.')
    # message get
    while(go):
        msg = q.get(isBlocking=True, timeout=2) # 큐가 비어있을 때 대기
        if msg is not None:
            msg_json = json.loads(msg.decode('utf-8'))
            if task_process is not None:
                task_process(msg_json)
    print('queue_listener is terminated.')


def create_listener():
    global handler
    handler = threading.Thread(target=queue_listener)
    handler.start()

def start():
    create_listener()
    return True


if __name__ == "__main__":
    queue_listener()
