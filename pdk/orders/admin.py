from django.contrib import admin

# Register your models here.
from .models import Pro_order, Pro_call


@admin.register(Pro_order)
class Order_admin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ("user",)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    list_display = ('产品名称', 'created_time', 'linkman', 'tel', 'state', 'user')
    list_filter = ('created_time',)
    search_fields = ('user__username', 'linkman', 'tel', 'pro_title__title')


@admin.register(Pro_call)
class Call_admin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(consultant=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ("consultant",)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.consultant = request.user
        obj.save()

    list_display = ('产品名称', 'contacts', 'telephone', 'state', 'created_time', 'is_display', 'consultant')
    list_filter = ('created_time',)
    search_fields = ('consultant__username', 'contacts', 'telephone')
