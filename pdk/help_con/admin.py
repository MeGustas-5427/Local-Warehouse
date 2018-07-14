from django.contrib import admin

from help_con.models import *

class Category_help_admin(admin.ModelAdmin):
    list_display = ('Category_tit', 'Category_des','index')

class Help_con_admin(admin.ModelAdmin):
    list_display = ('title', 'category','created_time')


class Help_sug_admin(admin.ModelAdmin):
    list_display = ('created_time','name','tel','state')



admin.site.register(Category_help,Category_help_admin)

admin.site.register(Help_con,Help_con_admin)

admin.site.register(Help_sug,Help_sug_admin)

