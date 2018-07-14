from django.contrib import admin
from demand.models import *

# Register your models here.

class demand_con_admin(admin.ModelAdmin):
    list_display = ('created_time','state','con_time','linkman','tel','password','type','message')
    list_filter = ('created_time',)

admin.site.register(demand_con,demand_con_admin)