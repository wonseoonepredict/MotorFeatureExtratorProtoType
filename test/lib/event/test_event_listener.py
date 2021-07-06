#!/usr/bin/env python
import lib.event.event_listener as EL
import patch
import fakeredis
import pytest

class FakeRedisQueue():
    def __init__(self,redis,key):
        self._redis = redis
        self._key = key

    def get(self,isBlocking=False,timeout=0):
        return self._redis.get(self._key)

@pytest.fixture(autouse=True)
def fredis():
    fake_redis = fakeredis.FakeStrictRedis()
    fake_redis.flushall()
    fake_redis.set('test','aaa')
    return FakeRedisQueue(fake_redis,"test")


@pytest.fixture()
def dummy_listener(fredis):
    listener = EL()
    EL.setredis(fredis)
    EL.create_listener()

def test_set_process_cb(fredis):
    val = fredis.get('111')

    print('val == ' + str(val))

    assert val == b'aaa'


def test_queue_listener():
    pass


