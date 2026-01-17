# apps/dyn_api/admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Property,
    Detector,
    Tenant,
    Utility,
  
    Key,
    Document,
    ExternalSurface,
    ExternalFeature,
    Boundary,
    CleaningStandard,
    DetectorCompliance,
    Room,
)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'postcode', 'property_type', 'detachment', 'view_report_link')
    list_display_links = ('id', 'address')
    search_fields = ('address', 'postcode')
    list_per_page = 25
    readonly_fields = ('view_report_link',)

    def view_report_link(self, obj):
        """
        Link to the public property report view.
        Uses the url name 'property_report' (args: pk). If your URL name differs,
        change the reverse() call or update the URL name in urls.py.
        """
        if not obj.pk:
            return "—"
        try:
            url = reverse("property_report", args=[obj.pk])
        except Exception:
            # fallback if reverse fails
            url = f"/properties/{obj.pk}/report/"
        return format_html('<a href="{}" target="_blank" rel="noopener">View report</a>', url)

    view_report_link.short_description = "Report"


class LinkedToPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'property',)
    search_fields = ('property__address',)
    list_filter = ('property',)


@admin.register(Tenant)
class TenantAdmin(LinkedToPropertyAdmin):
    pass


@admin.register(Utility)
class UtilityAdmin(LinkedToPropertyAdmin):
    pass


@admin.register(Detector)
class DetectorAdmin(LinkedToPropertyAdmin):
    pass




@admin.register(Key)
class KeyAdmin(LinkedToPropertyAdmin):
    pass


@admin.register(Document)
class DocumentAdmin(LinkedToPropertyAdmin):
    pass


@admin.register(ExternalSurface)
class ExternalSurfaceAdmin(LinkedToPropertyAdmin):
    pass


@admin.register(ExternalFeature)
class ExternalFeatureAdmin(LinkedToPropertyAdmin):
    pass


@admin.register(Boundary)
class BoundaryAdmin(LinkedToPropertyAdmin):
    pass


@admin.register(CleaningStandard)
class CleaningStandardAdmin(LinkedToPropertyAdmin):
    pass


@admin.register(DetectorCompliance)
class DetectorComplianceAdmin(LinkedToPropertyAdmin):
    pass


@admin.register(Room)
class RoomAdmin(LinkedToPropertyAdmin):
    pass
