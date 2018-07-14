from django.apps import AppConfig


class ProductConfig(AppConfig):
    name = 'product'
class AppNameConfig(AppConfig):
    name = 'news'
    verbose_name = u"产品中心"
    verbose_name_plural = u"产品中心"