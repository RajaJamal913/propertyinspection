from rest_framework import serializers
from .models import (
    Property, Tenant, Utility, DetectorCompliance, SmokeDetector,CoDetector,
    Key, Document, CleaningStandard, ExternalSurface,
    ExternalFeature, Boundary, Room, Door, Window, Ceiling, Floor,
    Wall, FixtureFitting, Furnishing, Cupboard, KitchenAppliance
)


# ----------- ROOM SUB-ENTITY SERIALIZERS -----------

class DoorSerializer(serializers.ModelSerializer):
    doorType = serializers.CharField(source="type")
    doorColour = serializers.CharField(source="colour")
    doorFinish = serializers.CharField(source="finish")
    frameType = serializers.CharField(source="frame_type")
    frameColour = serializers.CharField(source="frame_colour")
    photo = serializers.URLField(source="photo_url")

    class Meta:
        model = Door
        fields = [
            "id", "doorType", "doorFinish", "doorColour", "frameType", "frameColour",
            "features", "condition", "notes", "photo"
        ]


class WindowSerializer(serializers.ModelSerializer):
    windowType = serializers.CharField(source="type")
    glassType = serializers.CharField(source="glass_type")
    frameType = serializers.CharField(source="frame_type")
    frameColour = serializers.CharField(source="frame_colour")
    sillType = serializers.CharField(source="sill_type")
    sillColour = serializers.CharField(source="sill_colour")
    photo = serializers.URLField(source="photo_url")

    class Meta:
        model = Window
        fields = [
            "id", "windowType", "glassType", "frameType", "frameColour", "sillType",
            "sillColour", "condition", "features", "openers", "notes", "photo"
        ]


class CeilingSerializer(serializers.ModelSerializer):
    ceilingFinish = serializers.CharField(source="finish")
    ceilingFittings = serializers.CharField(source="fittings")
    recessedSpotlights = serializers.IntegerField(source="recessed_spotlights")
    bulbsNotWorking = serializers.IntegerField(source="bulbs_not_working")
    photo = serializers.URLField(source="photo_url")

    class Meta:
        model = Ceiling
        fields = [
            "id", "ceilingFinish", "colour", "condition", "ceilingFittings",
            "recessedSpotlights", "bulbsNotWorking", "notes", "photo"
        ]
        
class FloorSerializer(serializers.ModelSerializer):
    floorFinish = serializers.CharField(source="finish")
    photo = serializers.URLField(source="photo_url")

    class Meta:
        model = Floor
        fields = [
            "id", "floorFinish", "colour", "condition", "additions", "notes", "photo"
        ]
        
class WallSerializer(serializers.ModelSerializer):
    skirtingType = serializers.CharField(source="skirting_type")
    skirtingColour = serializers.CharField(source="skirting_colour")
    signOfLeakages = serializers.BooleanField(source="sign_of_leakages")
    photo = serializers.URLField(source="photo_url")

    class Meta:
        model = Wall
        fields = [
            "id", "description", "colour", "skirtingType", "skirtingColour",
            "condition", "features", "signOfLeakages", "notes", "photo"
        ]

class FixtureFittingSerializer(serializers.ModelSerializer):
    lightSwitches = serializers.IntegerField(source="light_switches")
    plugSockets = serializers.IntegerField(source="plug_sockets")
    lightFittings = serializers.IntegerField(source="light_fittings")
    lightTested = serializers.BooleanField(source="light_tested")
    plugSocketsTested = serializers.BooleanField(source="plug_sockets_tested")
    electricSwitchesVisuallySafe = serializers.BooleanField(source="electric_switches_safe")
    plugSocketsVisuallySafe = serializers.BooleanField(source="plug_sockets_safe")
    baseUnitDoors = serializers.IntegerField(source="base_unit_doors")
    wallUnits = serializers.IntegerField(source="wall_units")
    photo = serializers.URLField(source="photo_url")

    class Meta:
        model = FixtureFitting
        fields = [
            "id", "fixture", "notes", "lightSwitches", "plugSockets", "radiators",
            "lightFittings", "lightTested", "plugSocketsTested", "electricSwitchesVisuallySafe",
            "plugSocketsVisuallySafe", "toilets", "basins", "baseUnitDoors", "wallUnits",
            "worktops", "photo"
        ]

class FurnishingSerializer(serializers.ModelSerializer):
    photo = serializers.URLField(source="photo_url")

    class Meta:
        model = Furnishing
        fields = ["id", "furnishings", "notes", "photo"]
        

class CupboardSerializer(serializers.ModelSerializer):
    cupboardContent = serializers.CharField(source="contents")
    photo = serializers.URLField(source="photo_url")

    class Meta:
        model = Cupboard
        fields = ["id", "cupboardContent", "notes", "photo"]


class KitchenApplianceSerializer(serializers.ModelSerializer):
    kitchenAppliances = serializers.CharField(source="appliances")
    photo = serializers.URLField(source="photo_url")

    class Meta:
        model = KitchenAppliance
        fields = [
            "id", "kitchenAppliances", "brand", "colour", "condition",
            "quantity", "tested", "notes", "photo"
        ]
        
# ----------- ROOM SERIALIZER -----------

class RoomSerializer(serializers.ModelSerializer):
    roomType = serializers.CharField(source="name")
    photo = serializers.URLField(source="photo_url")
    doors = DoorSerializer(many=True)
    windows = WindowSerializer(many=True)
    ceilings = CeilingSerializer(many=True)
    floors = FloorSerializer(many=True)
    walls = WallSerializer(many=True)
    fixturesFittings = FixtureFittingSerializer(many=True, source="fixtures_fittings")
    furnishings = FurnishingSerializer(many=True)
    cupboards = CupboardSerializer(many=True)
    kitchenAppliances = KitchenApplianceSerializer(many=True, source="kitchen_appliances")

    class Meta:
        model = Room
        fields = [
            "id", "roomType", "notes", "photo",
            "doors", "windows", "ceilings", "floors", "walls",
            "fixturesFittings", "furnishings", "cupboards", "kitchenAppliances"
        ]
        
        
# ----------- OTHER RELATED SERIALIZERS -----------

class TenantSerializer(serializers.ModelSerializer):
    tenantName = serializers.CharField(source="name")
    tenantEmail = serializers.CharField(source="email")
    mobilePhone = serializers.CharField(source="mobile_phone")
    class Meta:
        model = Tenant
        fields = ["id", "tenantName","tenantEmail","mobilePhone", "notes"]
        extra_kwargs = {"property": {"read_only": True}}


class UtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Utility
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class DetectorComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectorCompliance
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class SmokeDetectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmokeDetector
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}
        
class CoDetectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoDetector
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class KeySerializer(serializers.ModelSerializer):
    photo = serializers.URLField(source="photo_url")
    class Meta:
        model = Key
        fields = ["id", "description", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


class DocumentSerializer(serializers.ModelSerializer):
    photo = serializers.URLField(source="photo_url")
    class Meta:
        model = Document
        fields = ["id", "description", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


class CleaningStandardSerializer(serializers.ModelSerializer):
    cleaningStandard = serializers.CharField(source="standard")
    class Meta:
        model = CleaningStandard
        fields = ["id", "cleaningStandard","notes"]
        extra_kwargs = {"property": {"read_only": True}}


class ExternalSurfaceSerializer(serializers.ModelSerializer):
    photo = serializers.URLField(source="photo_url")
    externalSurfaceType = serializers.CharField(source="type")
    class Meta:
        model = ExternalSurface
        fields = ["id", "externalSurfaceType","location", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


class ExternalFeatureSerializer(serializers.ModelSerializer):
    photo = serializers.URLField(source="photo_url")
    externalFeature = serializers.CharField(source="feature")
    class Meta:
        model = ExternalFeature
        fields = ["id", "externalFeature","condition", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


class BoundarySerializer(serializers.ModelSerializer):
    photo = serializers.URLField(source="photo_url")
    boundaryType = serializers.CharField(source="type")
    class Meta:
        model = Boundary
        fields = ["id", "boundaryType","colour","condition","quantity", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


# ----------- MAIN PROPERTY SERIALIZER -----------
class PropertySerializer(serializers.ModelSerializer):
    tenantDetails = TenantSerializer(source="tenants", many=True)
    utilities = UtilitySerializer(source="utility")
    smokeDetectors = SmokeDetectorSerializer(source="smoke_detectors", many=True)
    coDetectors = CoDetectorSerializer(source="co_detectors", many=True)  # corrected to plural and match field name
    detectorCompliance = DetectorComplianceSerializer(source="detector_compliance")
    keys = KeySerializer(many=True)
    documents = DocumentSerializer(many=True)
    cleaningStandard = CleaningStandardSerializer(source="cleaning_standard")
    externalSurfaces = ExternalSurfaceSerializer(source="external_surfaces", many=True)
    externalFeatures = ExternalFeatureSerializer(source="external_features", many=True)
    boundary = BoundarySerializer(source="boundaries", many=True)
    rooms = RoomSerializer(many=True)
    propertyType = serializers.CharField(source="property_type")
    inspectedBy = serializers.CharField()
    frontElevationPhoto = serializers.URLField(source="front_elevation_photos")
    otherViews = serializers.URLField(source="other_views")

    class Meta:
        model = Property
        fields = [
            "id", "address", "propertyType", "postcode", "detachment", "inspectedBy",
            "frontElevationPhoto", "otherViews", "documents",
            "externalSurfaces", "externalFeatures", "boundary", "rooms",
            "cleaningStandard", "keys", "smokeDetectors", "coDetectors", "detectorCompliance",
            "utilities", "tenantDetails"
        ]

    def create(self, validated_data):
        tenants_data = validated_data.pop("tenants", [])
        utility_data = validated_data.pop("utility", None)
        detector_compliance_data = validated_data.pop("detector_compliance", None)
        smoke_detectors_data = validated_data.pop("smoke_detectors", [])
        co_detectors_data = validated_data.pop("co_detectors", [])
        keys_data = validated_data.pop("keys", [])
        documents_data = validated_data.pop("documents", [])
        cleaning_standard_data = validated_data.pop("cleaning_standard", None)
        external_surfaces_data = validated_data.pop("external_surfaces", [])
        external_features_data = validated_data.pop("external_features", [])
        boundaries_data = validated_data.pop("boundaries", [])
        rooms_data = validated_data.pop("rooms", [])

        property_obj = Property.objects.create(**validated_data)

        for tenant in tenants_data:
            Tenant.objects.create(property=property_obj, **tenant)

        if utility_data:
            Utility.objects.create(property=property_obj, **utility_data)

        if detector_compliance_data:
            DetectorCompliance.objects.create(property=property_obj, **detector_compliance_data)

        for co in co_detectors_data:
            CoDetector.objects.create(property=property_obj, **co)

        for smokedetector in smoke_detectors_data:
            SmokeDetector.objects.create(property=property_obj, **smokedetector)

        for key in keys_data:
            Key.objects.create(property=property_obj, **key)

        for document in documents_data:
            Document.objects.create(property=property_obj, **document)

        if cleaning_standard_data:
            CleaningStandard.objects.create(property=property_obj, **cleaning_standard_data)

        for surface in external_surfaces_data:
            ExternalSurface.objects.create(property=property_obj, **surface)

        for feature in external_features_data:
            ExternalFeature.objects.create(property=property_obj, **feature)

        for boundary in boundaries_data:
            Boundary.objects.create(property=property_obj, **boundary)

        for room_data in rooms_data:
            doors_data = room_data.pop("doors", [])
            windows_data = room_data.pop("windows", [])
            ceilings_data = room_data.pop("ceilings", [])
            floors_data = room_data.pop("floors", [])
            walls_data = room_data.pop("walls", [])
            fixtures_fittings_data = room_data.pop("fixtures_fittings", [])
            furnishings_data = room_data.pop("furnishings", [])
            cupboards_data = room_data.pop("cupboards", [])
            appliances_data = room_data.pop("kitchen_appliances", [])

            room_obj = Room.objects.create(property=property_obj, **room_data)

            for door in doors_data:
                Door.objects.create(room=room_obj, **door)
            for window in windows_data:
                Window.objects.create(room=room_obj, **window)
            for ceiling in ceilings_data:
                Ceiling.objects.create(room=room_obj, **ceiling)
            for floor in floors_data:
                Floor.objects.create(room=room_obj, **floor)
            for wall in walls_data:
                Wall.objects.create(room=room_obj, **wall)
            for fixture in fixtures_fittings_data:
                FixtureFitting.objects.create(room=room_obj, **fixture)
            for furnishing in furnishings_data:
                Furnishing.objects.create(room=room_obj, **furnishing)
            for cupboard in cupboards_data:
                Cupboard.objects.create(room=room_obj, **cupboard)
            for appliance in appliances_data:
                KitchenAppliance.objects.create(room=room_obj, **appliance)

        return property_obj
