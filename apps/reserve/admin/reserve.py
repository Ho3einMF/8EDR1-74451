from django.contrib import admin

from apps.reserve.models import Reservation


@admin.register(Reservation)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "table", "individuals", "cost")
    search_fields = ("user__username", "table__number")
    autocomplete_fields = ("user", "table")
