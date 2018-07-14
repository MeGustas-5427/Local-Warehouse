#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.urls import path
from .views import *


app_name = 'cases_app'

urlpatterns = [
    path('list_case/', ListCaseView.as_view() , name='list_case'),
    path('detail_case/', detail_case , name='detail_case')
    ]