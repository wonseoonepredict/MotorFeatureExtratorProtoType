import json
import time as pytime
import sys
import threading
import signal

from lib.redis.redisqueue import RedisQueue


class EventListener:

    def __init__(self):
        self.go = True
        self.task_process = None
        self.q = None
        self.handle = None

    def con2redis(self):
        self.q = RedisQueue('my-queue', host='localhost', port=6379, db=0)

    def setredis(self, redis):
        self.q = redis

    def terminate(self):
        print('queue_listener will be terminated.')
        if self.handler is not None:
            self.go = False
            pytime.sleep(2)
            self.handler.join()


    def set_process_cb(self, process_cb):
        self.task_process = process_cb


    def queue_listener(self):
        print('queue_listener is created.')
        # message get
        while(self.go):
            msg = self.q.get(isBlocking=True, timeout=2) # 큐가 비어있을 때 대기
            if msg is not None:
                msg_json = json.loads(msg.decode('utf-8'))
                if self.task_process is not None:
                    self.task_process(msg_json)
        print('queue_listener is terminated.')


    def create_listener(self):
        self.handler = threading.Thread(target=self.queue_listener)
        self.handler.start()


event_listener = None


def start():
    global event_listener
    event_listener = EventListener() 
    event_listener.con2redis()
    event_listener.create_listener()
    return True


def terminate():
    print('-- requested to terminate. 0')
    print(event_listener)
    if event_listener is not None:
        print('-- requested to terminate. 1')
        event_listener.terminate()


def set_process_cb(process_cb):
    if event_listener is not None:
        event_listener.set_process_cb(process_cb)


if __name__ == "__main__":
    EventListener().queue_listener()
