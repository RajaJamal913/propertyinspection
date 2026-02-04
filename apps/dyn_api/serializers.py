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
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


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
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


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
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data
        
class FloorSerializer(serializers.ModelSerializer):
    floorFinish = serializers.CharField(source="finish")
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")


    class Meta:
        model = Floor
        fields = [
            "id", "floorFinish", "colour", "condition", "additions", "notes", "photo"
        ]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data
        
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
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data

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
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data
        

class CupboardSerializer(serializers.ModelSerializer):
    cupboardContent = serializers.CharField(source="contents")
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    class Meta:
        model = Cupboard
        fields = ["id", "cupboardContent", "notes", "photo"]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


class KitchenApplianceSerializer(serializers.ModelSerializer):
    kitchenAppliances = serializers.CharField(source="appliances")
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    class Meta:
        model = KitchenAppliance
        fields = [
            "id", "kitchenAppliances", "brand", "colour", "condition",
            "quantity", "tested", "notes", "photo"
        ]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data

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
    tenantEmail = serializers.CharField(source="email", allow_null=True, allow_blank=True, required=False)
    mobilePhone = serializers.CharField(source="mobile_phone", allow_null=True, allow_blank=True, required=False)
    class Meta:
        model = Tenant
        fields = ["id", "tenantName","tenantEmail","mobilePhone", "notes"]
        extra_kwargs = {"property": {"read_only": True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


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
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


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

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError

from .models import Detector


class CaseInsensitiveChoiceField(serializers.ChoiceField):
    """
    A ChoiceField that accepts case-insensitive keys or display labels
    and normalizes them to the canonical key (e.g. 'smoke' or 'co').
    """
    def to_internal_value(self, data):
        # keep normal null handling
        if data is None:
            return super().to_internal_value(data)

        # non-string values fall back to default handling (numbers, etc.)
        if not isinstance(data, str):
            return super().to_internal_value(data)

        norm = data.strip().lower()

        # Build (key, display) pairs from self.choices robustly
        items = []
        if isinstance(self.choices, dict):
            items = list(self.choices.items())
        else:
            try:
                items = list(self.choices)  # e.g. list of tuples
            except Exception:
                items = []

        # 1) Try matching keys case-insensitively
        for maybe_key, maybe_display in items:
            if str(maybe_key).lower() == norm:
                return super().to_internal_value(maybe_key)

        # 2) Try matching display labels case-insensitively
        for maybe_key, maybe_display in items:
            # maybe_display could itself be a tuple in some edge cases; coerce to str
            if str(maybe_display).lower() == norm:
                return super().to_internal_value(maybe_key)

        # fallback (will raise the standard ChoiceField ValidationError)
        return super().to_internal_value(data)


class DetectorSerializer(serializers.ModelSerializer):
    # existing strict field (keeps same external shape & source)
    detectorType = CaseInsensitiveChoiceField(
        source="detector_type",
        choices=Detector.DETECTOR_TYPE_CHOICES,
        required=False,
        allow_null=True
    )

    # NEW: human-friendly input field (write-only)
    detectorTypeLabel = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    detectorPresent = serializers.BooleanField(
        source="present", allow_null=True, required=False
    )

    photo = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Detector
        fields = [
            "id",
            "detectorType",        # canonical (read/write)
            "detectorTypeLabel",   # human input (write-only)
            "detectorPresent",
            "working",
            "location",
            "notes",
            "photo",
        ]
        extra_kwargs = {"property": {"read_only": True}}

    def validate(self, attrs):
        """
        Allow detectorTypeLabel to populate detector_type WITHOUT changing detectorType behavior.
        This runs after CaseInsensitiveChoiceField has attempted to set 'detector_type'.
        """
        label = attrs.pop("detectorTypeLabel", None)

        # Only populate detector_type from label when not already provided
        if label and not attrs.get("detector_type"):
            label_norm = label.strip().lower()

            label_map = {
                "smoke": "smoke",
                "smoke detector": "smoke",
                "smoke alarm": "smoke",
                "co": "co",
                "carbon monoxide": "co",
                "carbon monoxide detector": "co",
            }

            if label_norm not in label_map:
                raise serializers.ValidationError({
                    "detectorTypeLabel": f"'{label}' is not a valid detector type."
                })

            attrs["detector_type"] = label_map[label_norm]

        return attrs

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as exc:
            # convert DB integrity problems to serializer validation error
            raise DRFValidationError({"non_field_errors": [str(exc)]})

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as exc:
            raise DRFValidationError({"non_field_errors": [str(exc)]})
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


class KeySerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    class Meta:
        model = Key
        fields = ["id", "description", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


class DocumentSerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    class Meta:
        model = Document
        fields = ["id", "description", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


class CleaningStandardSerializer(serializers.ModelSerializer):
    cleaningStandard = serializers.CharField(source="standard",allow_null=True, required=False)
    class Meta:
        model = CleaningStandard
        fields = ["id", "cleaningStandard","notes"]
        extra_kwargs = {"property": {"read_only": True}}
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


class ExternalSurfaceSerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    externalSurfaceType = serializers.CharField(source="type")
    class Meta:
        model = ExternalSurface
        fields = ["id", "externalSurfaceType","location", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


class ExternalFeatureSerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    externalFeature = serializers.CharField(source="feature")
    class Meta:
        model = ExternalFeature
        fields = ["id", "externalFeature","condition", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


class BoundarySerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), source="photo_url")

    boundaryType = serializers.CharField(source="type")
    class Meta:
        model = Boundary
        fields = ["id", "boundaryType","colour","condition","quantity", "notes", "photo"]
        extra_kwargs = {"property": {"read_only": True}}
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove notes if empty or null
        if not data.get("notes"):
            data.pop("notes", None)
        return data


# ----------- MAIN PROPERTY SERIALIZER -----------
class PropertySerializer(serializers.ModelSerializer):
    tenantDetails = TenantSerializer(source="tenants", many=True)
    utilities = UtilitySerializer(source="utility")
    detectors = DetectorSerializer( many=True, required=False)
    detectorCompliance = DetectorComplianceSerializer(source="detector_compliance",required=False,        # <- don't require the whole nested object
    allow_null=True)
    keys = KeySerializer(many=True)
    documents = DocumentSerializer(many=True)
    cleaningStandard = CleaningStandardSerializer(source="cleaning_standard",allow_null=True, required=False)
    externalSurfaces = ExternalSurfaceSerializer(source="external_surfaces", many=True)
    externalFeatures = ExternalFeatureSerializer(source="external_features", many=True)
    boundary = BoundarySerializer(source="boundaries", many=True)
    rooms = RoomSerializer(many=True)
    propertyType = serializers.CharField(source="property_type")
    inspectedBy = serializers.CharField(allow_null=True, required=False)
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
