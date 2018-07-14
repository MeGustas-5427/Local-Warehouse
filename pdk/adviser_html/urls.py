#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.urls import path
from .views import *


app_name = 'adviser_app'

urlpatterns = [
    path('list_advise/', List_Adviser_View.as_view() , name='list_adviser'),
    path('aritcle_adviser/', article_adviser , name='article_adviser')
]