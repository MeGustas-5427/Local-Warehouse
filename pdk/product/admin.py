import os
import re
import time
import requests
from django.contrib import admin

from pdk.settings import BASE_DIR
from product.models import *


def get_header(link):
    host = re.search(r"://(?P<host>\S+?)/", link).group("host")
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': host,
        'Referer': link,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    return headers


class Category_pro_admin(admin.ModelAdmin):
    list_display = ('Category_pro_tit', 'Category_pro_des')


class Category_pro_son_admin(admin.ModelAdmin):
    list_display = ('Category_pro_tit', 'Category_pro_des')


class Category_pro_grandson_admin(admin.ModelAdmin):
    list_display = ('Category_pro_tit', 'Category_pro_des')


class Pro_content_admin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'count', 'created_time')
    search_fields = ['title']
    filter_horizontal = ('adviser', 'question', 'relation')

    def save_model(self, request, obj, form, change):
        if not os.path.exists(os.path.join(BASE_DIR, "new_img{}".format(time.strftime("/%Y/%m/%d/", time.localtime())))):
            os.makedirs(os.path.join(BASE_DIR, "new_img{}".format(time.strftime("/%Y/%m/%d/", time.localtime()))))
        for each_img_tag in re.findall(r'<img[\s\S]+?src="(?P<image>\S+?)"[\s\S]*?>', obj.body):
            if "https://img.pdk365.com/" in each_img_tag:
                continue
            try:
                image_name = each_img_tag.split("/")[-1]
                with open(os.path.join(os.path.join(BASE_DIR, "new_img{}".format(time.strftime("/%Y/%m/%d/", time.localtime()))), image_name), "wb") as img:
                    data = requests.get(each_img_tag, headers=get_header(each_img_tag)).content
                    img.write(data)
                obj.body = re.sub(r'<img([\s\S]+?)src="{}"([\s\S]*?)>'.format(each_img_tag), r'<img\1src="{}"\2>'.format("https://img.pdk365.com/"+"new_img{}".format(time.strftime("/%Y/%m/%d/", time.localtime()))+image_name), obj.body)
            except Exception:
                pass
        obj.save()


class Pro_question_admin(admin.ModelAdmin):
    list_display = ('ask', 'answer')


admin.site.register(Category_pro, Category_pro_admin)
admin.site.register(Category_pro_son, Category_pro_son_admin)
admin.site.register(Category_pro_grandson, Category_pro_grandson_admin)
admin.site.register(Pro_content, Pro_content_admin)
admin.site.register(Pro_question, Pro_question_admin)
