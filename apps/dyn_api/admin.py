from django.contrib import admin
from .models import (
    Property,
    Tenant,
    Utility,
    Detector,
    Key,
    Document,
    Inspector,
    ExternalSurface,
    ExternalFeature,
    Boundary,
    CleaningStandard,
    DetectorCompliance,
    Room,
)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'postcode', 'property_type', 'detachment')
    search_fields = ('address', 'postcode')


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

@admin.register(Inspector)
class InspectorAdmin(LinkedToPropertyAdmin):
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
