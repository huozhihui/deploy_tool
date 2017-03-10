#!/usr/bin/python
# -*- coding: utf-8 -*-
# 操作redis
import redis


def conn_redis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r

Rs = conn_redis()

class RedisResult:
    def __init__(self, tid):
        class Result:
            def __init__(self, key):
                self.key = key
                self.dict_value = Rs.hgetall(self.key)
                for k, v in self.dict_value.iteritems():
                    self.__dict__[k] = v

        self.obj_list = []
        pattern = "{tid}*".format(tid=tid)
        for key in Rs.scan_iter(match=pattern):
            self.obj_list.append(Result(key))

    def get_instance(self):
        return self.obj_list


if __name__ == "__main__":
    # redis_result = RedisResult("20170119162831-89-10.200.7.233")
    redis_result = RedisResult("20170119162831-89")
    print redis_result.get_instance()
    for res in redis_result.get_instance():
        print res.ip
        print res.state
        print res.stderr



