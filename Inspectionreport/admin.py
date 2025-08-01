# admin.py
from django.contrib import admin
from .models import (
    InspectionReport,
    PropertyDetails,
    TenantDetail,
    Utility,
    DetectorCompliance,
    SmokeDetector,
    CODetector,
    Key,
    Document,
    CleaningStandard,
    ExternalSurfaceType,
    ExternalFeature,
    Boundary,
    Room,
    Door,
    Window,
    Ceiling,
    Floor,
    Wall,
    FixtureFitting,
    Furnishing,
    Cupboard,
    KitchenAppliance,
)

# Optional: define inlines for nested relationships
class TenantDetailInline(admin.TabularInline):
    model = TenantDetail
    extra = 1

class UtilityInline(admin.StackedInline):
    model = Utility
    max_num = 1

class DetectorComplianceInline(admin.StackedInline):
    model = DetectorCompliance
    max_num = 1

class SmokeDetectorInline(admin.TabularInline):
    model = SmokeDetector
    extra = 1

class CODetectorInline(admin.TabularInline):
    model = CODetector
    extra = 1

class KeyInline(admin.TabularInline):
    model = Key
    extra = 1

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1

class PropertyDetailsAdmin(admin.ModelAdmin):
    inlines = [
        TenantDetailInline,
        UtilityInline,
        DetectorComplianceInline,
        SmokeDetectorInline,
        CODetectorInline,
        KeyInline,
        DocumentInline,
    ]
    list_display = ('address', 'postcode', 'propertyType', 'detachment')

class CleaningStandardAdmin(admin.ModelAdmin):
    list_display = ('cleaningStandard', 'report')

class ExternalSurfaceTypeAdmin(admin.ModelAdmin):
    list_display = ('report', 'location')

class ExternalFeatureAdmin(admin.ModelAdmin):
    list_display = ('report', 'condition')

class BoundaryAdmin(admin.ModelAdmin):
    list_display = ('report', 'boundaryType', 'quantity')

# Define Room inlines
class DoorInline(admin.TabularInline):
    model = Door
    extra = 1

class WindowInline(admin.TabularInline):
    model = Window
    extra = 1

class CeilingInline(admin.TabularInline):
    model = Ceiling
    extra = 1

class FloorInline(admin.TabularInline):
    model = Floor
    extra = 1

class WallInline(admin.TabularInline):
    model = Wall
    extra = 1

class FixtureFittingInline(admin.TabularInline):
    model = FixtureFitting
    extra = 1

class FurnishingInline(admin.TabularInline):
    model = Furnishing
    extra = 1

class CupboardInline(admin.TabularInline):
    model = Cupboard
    extra = 1

class KitchenApplianceInline(admin.TabularInline):
    model = KitchenAppliance
    extra = 1

class RoomAdmin(admin.ModelAdmin):
    inlines = [
        DoorInline,
        WindowInline,
        CeilingInline,
        FloorInline,
        WallInline,
        FixtureFittingInline,
        FurnishingInline,
        CupboardInline,
        KitchenApplianceInline,
    ]
    list_display = ('name', 'roomType', 'report')

# Register models
admin.site.register(InspectionReport)
admin.site.register(PropertyDetails, PropertyDetailsAdmin)
admin.site.register(CleaningStandard, CleaningStandardAdmin)
admin.site.register(ExternalSurfaceType, ExternalSurfaceTypeAdmin)
admin.site.register(ExternalFeature, ExternalFeatureAdmin)
admin.site.register(Boundary, BoundaryAdmin)
admin.site.register(Room, RoomAdmin)

# For simple models without inlines


# The inlined models and simple singletons
for model in [TenantDetail, Utility, DetectorCompliance, SmokeDetector,
              CODetector, Key, Document, Door, Window, Ceiling, Floor,
              Wall, FixtureFitting, Furnishing, Cupboard, KitchenAppliance]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
