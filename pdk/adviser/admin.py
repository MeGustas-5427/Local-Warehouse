from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from .models import adviser_user


@admin.register(adviser_user)
class User_Admin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'show')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('顾问信息'), {"fields": ('tel', 'profession', 'serve', 'thumbnail', 'excerpt', 'body')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined', 'show')
        return self.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user)
