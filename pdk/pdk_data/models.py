# encoding:utf-8
from django.db import models

# Create your models here.


class Data_access(models.Model):
    name_id = models.CharField('名称对应的id', max_length=100)
    type = models.CharField('类型', max_length=100)
    adviser_con = models.IntegerField('顾问询单量', blank=True,null=True)  # 顾问询单量
    adviser_order = models.IntegerField('顾问下单量', blank=True,null=True)  # 顾问下单量
    cases_count = models.IntegerField('案例访问量', blank=True,null=True) # 案例访问量
    news_count = models.IntegerField('案例访问量', blank=True,null=True) # 案例访问量
    product_count = models.IntegerField('产品下单量', blank=True,null=True) # 产品下单量

    created_time = models.DateTimeField('创建时间',auto_now_add=True)  # 创建时间