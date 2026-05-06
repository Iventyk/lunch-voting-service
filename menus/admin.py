from django.contrib import admin

from menus.models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "date", "updated_at")
    list_filter = ("date", "restaurant")
