from django.contrib import admin
from topic.models import *
# Register your models here.

class SpecialSubject_admin(admin.ModelAdmin):
    list_display = ('title','excerpt','created_time')
    search_fields =['title']
    list_filter = ('created_time',)


admin.site.register(SpecialSubject,SpecialSubject_admin)