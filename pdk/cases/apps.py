from django.apps import AppConfig


class CasesConfig(AppConfig):
    name = 'cases'

class AppNameConfig(AppConfig):
    name = 'news'
    verbose_name = u"��������"
    verbose_name_plural = verbose_name