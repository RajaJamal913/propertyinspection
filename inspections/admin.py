# inspections/admin.py
from django.contrib import admin
from .models import Inspection

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ("id", "inspected_by", "created_at")
    readonly_fields = ("created_at",)
    search_fields = ("inspected_by",)
