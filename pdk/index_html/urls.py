#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.urls import path
from .views import *


app_name = 'index_app'

urlpatterns = [
    path('', index, name='index')
]