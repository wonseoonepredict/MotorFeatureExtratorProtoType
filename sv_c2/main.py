#!/usr/bin/env python
import argparse
import os
import signal
import time

from lib.event.event_listener import start as listener_start
from lib.event.event_listener import terminate as listener_end
from sv_c2.task_process import process as task_process
from lib.event.event_listener import set_process_cb 

SUB_PROCESS_CNT=4

parentpid = 0

signals=[signal.SIGTERM, signal.SIGINT, signal.SIGSEGV]

clientpids=[]

def sig_handler(sig_num:int ,arg: int):
    # terminate listener thread
    listener_end()
    # terminate forked process
    if parentpid == os.getpid():
        if sig_num in signals:
            for pid in clientpids:
                os.kill(pid, sig_num)
    time.sleep(3)
    

def init():
    # set task_process_cb
    set_process_cb(task_process)
    # add signal
    for sig_num in signals:
        signal.signal(sig_num, sig_handler)
    # init listener thread
    listener_start()

def create_child():
    for i in range(0,SUB_PROCESS_CNT):
        pid = os.fork()
        if pid != 0:
            clientpids.append(pid)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', dest='worker')
    args = parser.parse_args()
    if args.worker is None:
        print('master node')
        parentpid = os.getpid()

        create_child()       

        if parentpid == os.getpid():
            print(clientpids)

        init();
    else:
        print('worker node')

if __name__=="__main__":
    main()
