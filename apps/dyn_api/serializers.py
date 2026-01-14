from rest_framework import serializers
from .models import (
    Property, Tenant, Utility, DetectorCompliance, SmokeDetector,CoDetector,
    Key, Document, CleaningStandard, ExternalSurface,
    ExternalFeature, Boundary, Room, Door, Window, Ceiling, Floor,
    Wall, FixtureFitting, Furnishing, Cupboard, KitchenAppliance
)


# ----------- ROOM SUB-ENTITY SERIALIZERS -----------
class DoorSerializer(serializers.ModelSerializer):
    doorType = serializers.CharField(source="type", required=False, allow_blank=True)
    doorColour = serializers.CharField(source="colour", required=False, allow_blank=True)
    doorFinish = serializers.CharField(source="finish", required=False, allow_blank=True)
    frameType = serializers.CharField(source="frame_type", required=False, allow_blank=True)
    frameColour = serializers.CharField(source="frame_colour", required=False, allow_blank=True)
    photo = serializers.ListField(
        child=serializers.URLField(), source="photo_url",
        required=False, allow_null=True, default=list
    )

    class Meta:
        model = Door
        fields = [
            "id", "doorType", "doorFinish", "doorColour", "frameType", "frameColour",
            "features", "condition", "notes", "photo"
        ]


class WindowSerializer(serializers.ModelSerializer):
    windowType = serializers.CharField(source="type", required=False, allow_blank=True)
    glassType = serializers.CharField(source="glass_type", required=False, allow_blank=True)
    frameType = serializers.CharField(source="frame_type", required=False, allow_blank=True)
    frameColour = serializers.CharField(source="frame_colour", required=False, allow_blank=True)
    sillType = serializers.CharField(source="sill_type", required=False, allow_blank=True)
    sillColour = serializers.CharField(source="sill_colour", required=False, allow_blank=True)
    photo = serializers.ListField(
        child=serializers.URLField(), source="photo_url",
        required=False, allow_null=True, default=list
    )

    class Meta:
        model = Window
        fields = [
            "id", "windowType", "glassType", "frameType", "frameColour", "sillType",
            "sillColour", "condition", "features", "openers", "notes", "photo"
        ]


class CeilingSerializer(serializers.ModelSerializer):
    ceilingFinish = serializers.CharField(source="finish", required=False, allow_blank=True)
    ceilingFittings = serializers.CharField(source="fittings", required=False, allow_blank=True)
    recessedSpotlights = serializers.IntegerField(source="recessed_spotlights", required=False, allow_null=True)
    bulbsNotWorking = serializers.IntegerField(source="bulbs_not_working", required=False, allow_null=True)
    photo = serializers.ListField(
        child=serializers.URLField(), source="photo_url",
        required=False, allow_null=True, default=list
    )

    class Meta:
        model = Ceiling
        fields = [
            "id", "ceilingFinish", "colour", "condition", "ceilingFittings",
            "recessedSpotlights", "bulbsNotWorking", "notes", "photo"
        ]

        
class FloorSerializer(serializers.ModelSerializer):
    floorFinish = serializers.CharField(source="finish", required=False, allow_blank=True)
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
    tenantDetails = TenantSerializer(source="tenants", many=True, required=False, default=list)
    utilities = UtilitySerializer(source="utility", required=False, allow_null=True)
    smokeDetectors = SmokeDetectorSerializer(source="smoke_detectors", many=True, required=False, default=list)
    coDetectors = CoDetectorSerializer(source="co_detectors", many=True, required=False, default=list)
    detectorCompliance = DetectorComplianceSerializer(source="detector_compliance", required=False, allow_null=True)
    keys = KeySerializer(many=True, required=False, default=list)
    documents = DocumentSerializer(many=True, required=False, default=list)
    cleaningStandard = CleaningStandardSerializer(source="cleaning_standard", required=False, allow_null=True)
    externalSurfaces = ExternalSurfaceSerializer(source="external_surfaces", many=True, required=False, default=list,allow_null=True)
    externalFeatures = ExternalFeatureSerializer(source="external_features", many=True, required=False, default=list,allow_null=True)
    boundary = BoundarySerializer(source="boundaries", many=True, required=False, default=list,allow_null=True)
    rooms = RoomSerializer(many=True, required=False, default=list)
    propertyType = serializers.CharField(source="property_type")
    inspectedBy = serializers.CharField(required=False, allow_blank=True)
    frontElevationPhoto = serializers.ListField(
        child=serializers.URLField(), source="front_elevation_photos", required=False, default=list
    )
    otherViews = serializers.ListField(
        child=serializers.URLField(), source="other_views", required=False, default=list
    )

    class Meta:
        model = Property
        fields = [
            "id", "address", "propertyType", "postcode", "detachment", "inspectedBy",
            "frontElevationPhoto", "otherViews", "documents",
            "externalSurfaces", "externalFeatures", "boundary", "rooms",
            "cleaningStandard", "keys", "smokeDetectors", "coDetectors", "detectorCompliance",
            "utilities", "tenantDetails"
        ]

    def validate(self, data):
        """
        Enforce:
         - Kitchen rooms must include fixtures_fittings and kitchen_appliances (as lists).
         - Non-kitchen rooms must NOT include those fields.
         - Provide room-indexed errors for clearer client responses.
         - Validate top-level list fields are lists (defensive).
        """
        errors = {}

        # Defensive checks for top-level list fields (ListField usually validates this,
        # but explicit checks produce clearer error keys).
        if "front_elevation_photos" in data and not isinstance(data["front_elevation_photos"], list):
            errors["front_elevation_photos"] = "front_elevation_photos must be a list of image URLs."

        if "other_views" in data and not isinstance(data["other_views"], list):
            errors["other_views"] = "other_views must be a list of image URLs."

        rooms = data.get("rooms", [])
        if rooms is not None and not isinstance(rooms, list):
            errors["rooms"] = "rooms must be a list of room objects."

        # Validate each room and collect per-room errors
        room_level_errors = []
        if isinstance(rooms, list):
            for idx, room in enumerate(rooms):
                room_err = {}
                if not isinstance(room, dict):
                    room_err["__all__"] = "Each room must be an object/dictionary."
                    room_level_errors.append(room_err)
                    continue

                # Normalize room type key (incoming may be 'name' or 'roomType')
                room_type = (room.get("name") or room.get("roomType") or "").strip()
                is_kitchen = room_type.lower() == "kitchen" if room_type else False

                # For kitchens: fixtures_fittings AND kitchen_appliances must be present and lists
                if is_kitchen:
                    ff = room.get("fixtures_fittings")
                    ka = room.get("kitchen_appliances")

                    if not ff:
                        room_err["fixtures_fittings"] = "Kitchen must include 'fixtures_fittings' (list)."
                    elif not isinstance(ff, list):
                        room_err["fixtures_fittings"] = "fixtures_fittings must be a list."

                    if not ka:
                        room_err["kitchen_appliances"] = "Kitchen must include 'kitchen_appliances' (list)."
                    elif not isinstance(ka, list):
                        room_err["kitchen_appliances"] = "kitchen_appliances must be a list."

                # For non-kitchens: these fields must NOT be present (or must be empty)
                else:
                    if "fixtures_fittings" in room and room.get("fixtures_fittings"):
                        room_err["fixtures_fittings"] = "Only kitchens may include 'fixtures_fittings'."
                    if "kitchen_appliances" in room and room.get("kitchen_appliances"):
                        room_err["kitchen_appliances"] = "Only kitchens may include 'kitchen_appliances'."

                # Optionally validate nested simple types (e.g., photo lists) within room
                # e.g., ensure room['photo_url'] if provided is a list
                if "photo_url" in room and room.get("photo_url") is not None and not isinstance(room.get("photo_url"), list):
                    room_err["photo_url"] = "photo_url must be a list of image URLs."

                room_level_errors.append(room_err if room_err else None)

        # If any room-level errors exist, attach them
        if any(x for x in room_level_errors if x):
            errors["rooms"] = room_level_errors

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        # keep existing create logic (safe pops with defaults)
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
