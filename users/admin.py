from django.contrib import admin

from users.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "created_at")
    search_fields = ("full_name", "user__username", "user__email")
