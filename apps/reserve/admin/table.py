from django.contrib import admin

from apps.reserve.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "capacity", "is_reserved")
    search_fields = ("number",)
    list_filter = ("is_reserved",)
