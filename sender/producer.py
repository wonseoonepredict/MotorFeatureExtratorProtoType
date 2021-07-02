from lib.redis.redisqueue import RedisQueue

q = RedisQueue('my-queue', host='localhost', port=6379, db=0)


if __name__ == "__main__":
    # message put
    import json
    import time as pytime
    for i in range(30):
        cur_time = '{"timestamp":' + str(pytime.time()) + '}'
        element = json.loads(cur_time)

        # Add Your Own Data
        element['id'] = i

        element_str = json.dumps(element)
        print(element_str)
        q.put(element_str)
