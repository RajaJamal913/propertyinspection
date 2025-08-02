from rest_framework import serializers
from .models import (
    Property, Tenant, Utility, DetectorCompliance, Detector,
    Key, Document, CleaningStandard, Inspector, ExternalSurface,
    ExternalFeature, Boundary, Room, Door, Window, Ceiling, Floor,
    Wall, FixtureFitting, Furnishing, Cupboard, KitchenAppliance
)


# ----------- ROOM SUB-ENTITY SERIALIZERS -----------

class DoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = "__all__"
        extra_kwargs = {"room": {"read_only": True}}


class WindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Window
        fields = "__all__"
        extra_kwargs = {"room": {"read_only": True}}


class CeilingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceiling
        fields = "__all__"
        extra_kwargs = {"room": {"read_only": True}}


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = "__all__"
        extra_kwargs = {"room": {"read_only": True}}


class WallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wall
        fields = "__all__"
        extra_kwargs = {"room": {"read_only": True}}


class FixtureFittingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixtureFitting
        fields = "__all__"
        extra_kwargs = {"room": {"read_only": True}}


class FurnishingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furnishing
        fields = "__all__"
        extra_kwargs = {"room": {"read_only": True}}


class CupboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupboard
        fields = "__all__"
        extra_kwargs = {"room": {"read_only": True}}


class KitchenApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenAppliance
        fields = "__all__"
        extra_kwargs = {"room": {"read_only": True}}


# ----------- ROOM SERIALIZER -----------

class RoomSerializer(serializers.ModelSerializer):
    doors = DoorSerializer(many=True)
    windows = WindowSerializer(many=True)
    ceilings = CeilingSerializer(many=True)
    floors = FloorSerializer(many=True)
    walls = WallSerializer(many=True)
    fixtures_fittings = FixtureFittingSerializer(many=True)
    furnishings = FurnishingSerializer(many=True)
    cupboards = CupboardSerializer(many=True)
    kitchen_appliances = KitchenApplianceSerializer(many=True)

    class Meta:
        model = Room
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


# ----------- OTHER RELATED SERIALIZERS -----------

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = "__all__"
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


class DetectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detector
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class CleaningStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningStandard
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class InspectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspector
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class ExternalSurfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSurface
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class ExternalFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalFeature
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


class BoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Boundary
        fields = "__all__"
        extra_kwargs = {"property": {"read_only": True}}


# ----------- MAIN PROPERTY SERIALIZER -----------

class PropertySerializer(serializers.ModelSerializer):
    tenants = TenantSerializer(many=True)
    utilities = UtilitySerializer(many=True)
    detector_compliance = DetectorComplianceSerializer()
    detectors = DetectorSerializer(many=True)
    keys = KeySerializer(many=True)
    documents = DocumentSerializer(many=True)
    cleaning_standard = CleaningStandardSerializer()
    inspectors = InspectorSerializer(many=True)
    external_surfaces = ExternalSurfaceSerializer(many=True)
    external_features = ExternalFeatureSerializer(many=True)
    boundaries = BoundarySerializer(many=True)
    rooms = RoomSerializer(many=True)

    class Meta:
        model = Property
        fields = "__all__"

    def create(self, validated_data):
        tenants_data = validated_data.pop("tenants", [])
        utilities_data = validated_data.pop("utilities", [])
        detector_compliance_data = validated_data.pop("detector_compliance", None)
        detectors_data = validated_data.pop("detectors", [])
        keys_data = validated_data.pop("keys", [])
        documents_data = validated_data.pop("documents", [])
        cleaning_standard_data = validated_data.pop("cleaning_standard", None)
        inspectors_data = validated_data.pop("inspectors", [])
        external_surfaces_data = validated_data.pop("external_surfaces", [])
        external_features_data = validated_data.pop("external_features", [])
        boundaries_data = validated_data.pop("boundaries", [])
        rooms_data = validated_data.pop("rooms", [])

        property_obj = Property.objects.create(**validated_data)

        for tenant in tenants_data:
            Tenant.objects.create(property=property_obj, **tenant)

        for utility in utilities_data:
            Utility.objects.create(property=property_obj, **utility)

        if detector_compliance_data:
            DetectorCompliance.objects.create(property=property_obj, **detector_compliance_data)

        for detector in detectors_data:
            Detector.objects.create(property=property_obj, **detector)

        for key in keys_data:
            Key.objects.create(property=property_obj, **key)

        for document in documents_data:
            Document.objects.create(property=property_obj, **document)

        if cleaning_standard_data:
            CleaningStandard.objects.create(property=property_obj, **cleaning_standard_data)

        for inspector in inspectors_data:
            Inspector.objects.create(property=property_obj, **inspector)

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
