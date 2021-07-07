#!/usr/bin/env python
import patch
import fakeredis
import pytest
import time

from lib.event.event_listener import EventListener as EL


processed_data = ''


class FakeRedisQueue():

    def __init__(self,redis,key: str):
        self._redis = redis
        self._key = key


    def get(self,isBlocking: bool = False,timeout: int = 0):
        return self._redis.get(self._key)


    def setwithkey(self, key: str, msg: str):
        import json
        jsons = '{"msg":' + '"' + msg +'"}'
        self._redis.set(key, jsons)


    def set(self, msg: str):
        self.setwithkey(self._key, msg)


@pytest.fixture(autouse=True)
def fredis():

    fake_redis = fakeredis.FakeStrictRedis()
    fake_redis.flushall()
    return FakeRedisQueue(fake_redis,"test")


@pytest.fixture(autouse=True)
def dummy_listener(fredis):

    listener = EL()
    listener.setredis(fredis)

    return listener


def test_redis_queue(fredis):

    fredis.set('aaa')
    val = fredis.get('111')

    assert val == b'{"msg":"aaa"}'


def test_queue_listener(fredis, dummy_listener):
    def test_cb(msg):
        import json
        global processed_data
        processed_data = msg['msg']

    fredis.set('aaa')
    dummy_listener.set_process_cb(test_cb)
    dummy_listener.create_listener()
    time.sleep(1)
    dummy_listener.terminate()

    assert processed_data == 'aaa'
