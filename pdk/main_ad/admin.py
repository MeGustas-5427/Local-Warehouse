from django.contrib import admin

from main_ad.models import Carousel,Index_news,Main_banner,Menu_nav_ad,Index_banner_ad


class Carousel_admin(admin.ModelAdmin):
    list_display = ('name', 'url','index','created_time')
    list_editable = ('index',)

class Index_news_admin(admin.ModelAdmin):
    list_display = ('name', 'url','index','created_time')
    list_editable = ('index',)

class Main_banner_admin(admin.ModelAdmin):
    list_display = ('name', 'url','index','created_time')
    list_editable = ('index',)
    filter_horizontal = ('category','category_son','category_grandson')

class Menu_nav_ad_admin(admin.ModelAdmin):
    list_display = ('name', 'url','index','created_time')
    list_editable = ('index',)

class Index_banner_ad_admin(admin.ModelAdmin):
    list_display = ('name', 'url','index','created_time')
    list_editable = ('index',)



admin.site.register(Carousel,Carousel_admin)
admin.site.register(Index_news,Index_news_admin)
admin.site.register(Main_banner,Main_banner_admin)
admin.site.register(Menu_nav_ad,Menu_nav_ad_admin)
admin.site.register(Index_banner_ad,Index_banner_ad_admin)
