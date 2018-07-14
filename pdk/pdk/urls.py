# encoding:utf-8

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from help_html.views import help

urlpatterns = [
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('', admin.site.urls),
    path('index/', include('index_html.urls')),
    path('', include('adviser_html.urls')),
    path('', include('product.urls')),
    path('', include('cases.urls')),
    path('help/', help, name='help'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


admin.site.site_title = '跑得快企服超市'
admin.site.index_title = '跑得快企服超市'