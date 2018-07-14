from django.contrib import admin
from django.contrib.auth.models import Group
from cases.models import Cases_con


class Cases_con_admin(admin.ModelAdmin):
    list_display = ('title', 'auditing','category','created_time')
    search_fields = ['title']
    list_filter = ('created_time','auditing')
    filter_horizontal = ('pro',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            if Group.objects.get(user=request.user).__str__() == "顾问":
                return ("auditing", "adviser","index_show")
            elif Group.objects.get(user=request.user).__str__() == "审核组":
                return ("adviser", )
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        try:
            if Group.objects.get(user=request.user).__str__() == "顾问":
                obj.adviser = request.user
        except Exception:
            pass
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(adviser=request.user)


admin.site.register(Cases_con, Cases_con_admin)
