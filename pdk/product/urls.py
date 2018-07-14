#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.urls import path
from .views import *


app_name = 'product_app'

urlpatterns = [
    path('list_product/', ListProductView.as_view() , name='list_product'),
    path('detail_product/', detail_product , name='detail_product')
    ]