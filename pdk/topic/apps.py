# encoding:utf-8
from django.apps import AppConfig


class TopicConfig(AppConfig):
    name = 'topic'



class AppNameConfig(AppConfig):
    name = 'news'
    verbose_name = u"专题管理"
    verbose_name_plural = u"专题管理"