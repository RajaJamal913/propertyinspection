from rest_framework import serializers
from .models import (
    Property, Tenant, Utility, DetectorCompliance, 
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
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")


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
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")


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
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")


    class Meta:
        model = Ceiling
        fields = [
            "id", "ceilingFinish", "colour", "condition", "ceilingFittings",
            "recessedSpotlights", "bulbsNotWorking", "notes", "photo"
        ]
        
class FloorSerializer(serializers.ModelSerializer):
    floorFinish = serializers.CharField(source="finish")
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")


    class Meta:
        model = Floor
        fields = [
            "id", "floorFinish", "colour", "condition", "additions", "notes", "photo"
        ]
        
class WallSerializer(serializers.ModelSerializer):
    skirtingType = serializers.CharField(source="skirting_type")
    skirtingColour = serializers.CharField(source="skirting_colour")
    signOfLeakages = serializers.BooleanField(source="sign_of_leakages")
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")


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
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")


    class Meta:
        model = FixtureFitting
        fields = [
            "id", "fixture", "notes", "lightSwitches", "plugSockets", "radiators",
            "lightFittings", "lightTested", "plugSocketsTested", "electricSwitchesVisuallySafe",
            "plugSocketsVisuallySafe", "toilets", "basins", "baseUnitDoors", "wallUnits",
            "worktops", "photo"
        ]

class FurnishingSerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")


    class Meta:
        model = Furnishing
        fields = ["id", "furnishings", "notes", "photo"]
        

class CupboardSerializer(serializers.ModelSerializer):
    cupboardContent = serializers.CharField(source="contents")
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    class Meta:
        model = Cupboard
        fields = ["id", "cupboardContent", "notes", "photo"]


class KitchenApplianceSerializer(serializers.ModelSerializer):
    kitchenAppliances = serializers.CharField(source="appliances")
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    class Meta:
        model = KitchenAppliance
        fields = [
            "id", "kitchenAppliances", "brand", "colour", "condition",
            "quantity", "tested", "notes", "photo"
        ]
        
# ----------- ROOM SERIALIZER -----------

class RoomSerializer(serializers.ModelSerializer):
    roomType = serializers.CharField(source="name")
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")
    doors = DoorSerializer(many=True)
    windows = WindowSerializer(many=True)
    ceilings = CeilingSerializer(many=True)
    floors = FloorSerializer(many=True)
    walls = WallSerializer(many=True)
    # 🔑 Important: add source to link with related_name
    fixturesFittings = FixtureFittingSerializer(
        many=True, required=False, allow_null=True, default=list, source="fixtures_fittings"
    )
    kitchenAppliances = KitchenApplianceSerializer(
        many=True, required=False, allow_null=True, default=list, source="kitchen_appliances"
    )
    furnishings = FurnishingSerializer(many=True)
    cupboards = CupboardSerializer(many=True)

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


from rest_framework import serializers
from .models import Utility

class UtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Utility
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in list(self.fields.items()):
            # keep property read-only as requested
            if name == "property":
                continue
            # Do not require fields on input
            field.required = False
            # Allow None for fields that support it
            if hasattr(field, "allow_null"):
                field.allow_null = True
            # Allow empty strings for CharFields
            if isinstance(field, serializers.CharField):
                field.allow_blank = True


class DetectorComplianceSerializer(serializers.ModelSerializer):
    # expose camelCase JSON keys while mapping to snake_case model fields
    smokeAlarmCompliance = serializers.CharField(
        source="smoke_alarm_compliance", allow_blank=True, required=False
    )
    carbonMonoxideCompliance = serializers.CharField(
        source="carbon_monoxide_compliance", allow_blank=True, required=False
    )

    class Meta:
        model = DetectorCompliance
        # explicit list prevents duplicate snake_case fields in the output
        fields = ("id", "smokeAlarmCompliance", "carbonMonoxideCompliance", "property")
        extra_kwargs = {"property": {"read_only": True}}


# serializers.py (add)
from rest_framework import serializers
from .models import Detector

class DetectorSerializer(serializers.ModelSerializer):
    detectorType = serializers.ChoiceField(source="detector_type", choices=Detector.DETECTOR_TYPE_CHOICES)
    detectorPresent = serializers.BooleanField(source="present", allow_null=True, required=False)
    photo = serializers.ListField(child=serializers.URLField(), required=False)

    class Meta:
        model = Detector
        fields = ["id", "detectorType", "detectorPresent", "working", "location", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


class KeySerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    class Meta:
        model = Key
        fields = ["id", "description", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


class DocumentSerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

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
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    externalSurfaceType = serializers.CharField(source="type")
    class Meta:
        model = ExternalSurface
        fields = ["id", "externalSurfaceType","location", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


class ExternalFeatureSerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    externalFeature = serializers.CharField(source="feature")
    class Meta:
        model = ExternalFeature
        fields = ["id", "externalFeature","condition", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


class BoundarySerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    boundaryType = serializers.CharField(source="type")
    class Meta:
        model = Boundary
        fields = ["id", "boundaryType","colour","condition","quantity", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}


# ----------- MAIN PROPERTY SERIALIZER -----------
class PropertySerializer(serializers.ModelSerializer):
    tenantDetails = TenantSerializer(source="tenants", many=True)
    utilities = UtilitySerializer(source="utility")
    detectors = DetectorSerializer( many=True, required=False)
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
    frontElevationPhoto = serializers.ListField(child=serializers.URLField(), source="front_elevation_photos")
    otherViews = serializers.ListField(child=serializers.URLField(), source="other_views")
    
    class Meta:
        model = Property
        fields = [
            "id", "address", "propertyType", "postcode", "detachment", "inspectedBy",
            "frontElevationPhoto", "otherViews", "documents",
            "externalSurfaces", "externalFeatures", "boundary", "rooms",
            "cleaningStandard", "keys", "detectors",   "detectorCompliance",
            "utilities", "tenantDetails"
        ]
        
    def validate(self, data):
        """
        Enforce kitchen rules:
        - If room type is Kitchen → fixtures_fittings and kitchen_appliances are required.
        - Otherwise → they must not be present.
        """
        rooms = data.get("rooms", [])
        for room in rooms:
            room_type = room.get("name") or room.get("roomType")  # serializer mapping

            if room_type and room_type.lower() == "kitchen":
                if not room.get("fixtures_fittings"):
                    raise serializers.ValidationError({
                        "rooms": f"Room '{room_type}' must include fixture and fittings."
                    })
                if not room.get("kitchen_appliances"):
                    raise serializers.ValidationError({
                        "rooms": f"Room '{room_type}' must include kitchen appliances."
                    })
            else:
                if room.get("fixtures_fittings"):
                    raise serializers.ValidationError({
                        "rooms": f"Room '{room_type}' cannot have fixture and fittings (only for kitchen)."
                    })
                if room.get("kitchen_appliances"):
                    raise serializers.ValidationError({
                        "rooms": f"Room '{room_type}' cannot have kitchen appliances (only for kitchen)."
                    })
        return data

    def create(self, validated_data):
        tenants_data = validated_data.pop("tenants", [])
        utility_data = validated_data.pop("utility", None)
        detector_compliance_data = validated_data.pop("detector_compliance", None)
        detectors_data = validated_data.pop("detectors", []) 
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

        for d in detectors_data:
            # d keys will be like {'detector_type': 'smoke', 'present': True, 'working': True, ...}
            Detector.objects.create(property=property_obj, **d)

        
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
