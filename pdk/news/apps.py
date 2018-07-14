# encoding:utf-8

from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class NewsConfig(AppConfig):
    name = 'news'

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'

class AppNameConfig(AppConfig):
    name = 'news'
    verbose_name = u"新闻中心"
    verbose_name_plural = u"新闻中心"