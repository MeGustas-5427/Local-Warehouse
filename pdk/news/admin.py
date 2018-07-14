
from django.contrib import admin

from news.models import *


class Category_news_admin(admin.ModelAdmin):
    list_display = ('Category_news_tit', 'Category_news_des')


class News_con_admin(admin.ModelAdmin):
    list_display = ('title', 'category', 'excerpt', 'created_time')
    search_fields = ['title']
    list_filter = ('created_time',)


admin.site.register(News_con, News_con_admin)
admin.site.register(Category_news, Category_news_admin)
