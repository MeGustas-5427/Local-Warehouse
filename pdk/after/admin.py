from django.contrib import admin
from after.models import tema,line_tema,after_ask

# Register your models here.
class tema_admin(admin.ModelAdmin):
    list_display = ('tit', 'des')
    filter_horizontal = ('name','category','category_son','category_grandson','pro')

#
class line_tema_admin(admin.ModelAdmin):
    list_display = ('tit', 'des')
    filter_horizontal = ('category','category_son','category_grandson','pro')


class after_ask_admin(admin.ModelAdmin):
    list_display = ('ask','answer')
    filter_horizontal = ('category', 'category_son', 'category_grandson', 'pro')

admin.site.register(tema,tema_admin)
admin.site.register(line_tema,line_tema_admin)
admin.site.register(after_ask,after_ask_admin)