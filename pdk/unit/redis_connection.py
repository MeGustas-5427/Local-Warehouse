#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import redis
from .config import HOST2
from django.http import HttpResponse

redis_db1 = redis.StrictRedis(host=HOST2,
                              port=6379,
                              db=1,
                              decode_responses=True,
                              password="HuiDao88558853"
                              )

redis_db14 = redis.StrictRedis(host=HOST2,
                              port=6379,
                              db=14,
                              decode_responses=True,
                              password="HuiDao88558853"
                              )

def redis_result(url):
    result = redis_db1.get(url)
    if result:
        return HttpResponse(result)
    else:
        return None


def redis_save_render_template(url,html):
    redis_db1.setex(url, 1000, html.content)  # 1000秒后过期