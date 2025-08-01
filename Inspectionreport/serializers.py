from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import (
    InspectionReport, PropertyDetails, TenantDetail, Utility,
    DetectorCompliance, SmokeDetector, CODetector, Key, Document,
    CleaningStandard, ExternalSurfaceType, ExternalFeature, Boundary,
    Room, Door, Window, Ceiling, Floor, Wall, FixtureFitting,
    Furnishing, Cupboard, KitchenAppliance
)

class TenantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantDetail
        fields = ['tenantName', 'tenantEmail', 'mobilePhone', 'notes']

class UtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Utility
        fields = [
            'gasMeterReading', 'gasMeterSerialNumber', 'gasMeterPhoto',
            'electricityMeterReading', 'electricityMeterSerialNumber', 'electricityMeterPhoto',
            'waterMeterReading', 'waterMeterSerialNumber', 'waterMeterPhoto',
            'heatMeterReading', 'heatMeterSerialNumber', 'heatMeterPhoto',
            'otherMeterType', 'otherMeterReading', 'otherMeterSerialNumber', 'otherMeterPhoto',
            'stopcokLocation', 'stopcokPhoto', 'fuseboxLocation', 'fuseboxPhoto', 'notes'
        ]

class DetectorComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectorCompliance
        fields = ['detectorCompliance', 'solidFuelDevice']

class SmokeDetectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmokeDetector
        fields = ['smokeDetector', 'working', 'location', 'notes']

class CODetectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CODetector
        fields = ['coDetector', 'working', 'location', 'notes']

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ['description', 'notes', 'photo']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['description', 'notes', 'photo']

class PropertyDetailsSerializer(WritableNestedModelSerializer):
    tenantDetails = TenantDetailSerializer(many=True)
    utilitites = UtilitySerializer()
    detectorCompliance = DetectorComplianceSerializer()
    smokeDetector = SmokeDetectorSerializer(many=True)
    coDetector = CODetectorSerializer(many=True)
    keys = KeySerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = PropertyDetails
        fields = [
            'address', 'postcode', 'propertyType', 'detachment',
            'frontElevationPhoto', 'otherViews', 'tenantDetails',
            'utilitites', 'detectorCompliance', 'smokeDetector',
            'coDetector', 'keys', 'documents'
        ]

class CleaningStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningStandard
        fields = ['cleaningStandard', 'notes']

class ExternalSurfaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSurfaceType
        fields = ['externalSurfaceType', 'location', 'notes', 'photo']

class ExternalFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalFeature
        fields = ['externalFeatures', 'condition', 'notes', 'photo']

class BoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Boundary
        fields = ['boundaryType', 'colour', 'condition', 'quantity', 'notes', 'photo']

class DoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = [
            'makeDefaultDoor', 'doorType', 'doorFinish', 'doorColour',
            'frameType', 'frameColour', 'features', 'condition', 'notes', 'photo'
        ]

class WindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Window
        fields = [
            'makeDefaultWindow', 'windowType', 'glassType', 'frameType',
            'frameColour', 'sillType', 'sillColour', 'condition',
            'features', 'openers', 'notes', 'photo'
        ]

class CeilingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceiling
        fields = [
            'makeDefaultCeiling', 'ceilingFinish', 'colour', 'condition',
            'ceilingFittings', 'recessedSpotlights', 'bulbsNotWorking',
            'notes', 'photo'
        ]

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = [
            'makeDefaultFloor', 'floorFinish', 'colour', 'condition',
            'additions', 'notes', 'photo'
        ]

class WallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wall
        fields = [
            'makeDefaultWall', 'description', 'colour', 'skirtingType',
            'skirtingColour', 'condition', 'features', 'signOfLeakages',
            'notes', 'photo'
        ]

class FixtureFittingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixtureFitting
        fields = [
            'fixture', 'notes', 'lightSwitches', 'plugSockets', 'radiators',
            'loghtFittings', 'lightTested', 'plugSocketsTested',
            'electricSwitchesVisualluSafe', 'PlugSocketsVisuallySafe',
            'toilets', 'basins', 'baseUnitDoors', 'wallUnits', 'worktops', 'photo'
        ]

class FurnishingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furnishing
        fields = ['furnishing', 'notes', 'photo']

class CupboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupboard
        fields = ['cupboardContent', 'notes', 'photo']

class KitchenApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenAppliance
        fields = [
            'kitchenAppliances', 'brand', 'colour', 'condition',
            'quantity', 'tested', 'notes', 'photo'
        ]

class RoomSerializer(WritableNestedModelSerializer):
    doors = DoorSerializer(many=True)
    windows = WindowSerializer(many=True)
    ceilings = CeilingSerializer(many=True)
    floors = FloorSerializer(many=True)
    walls = WallSerializer(many=True)
    fixturesFittings = FixtureFittingSerializer(many=True)
    furnishing = FurnishingSerializer(many=True)
    cupboard = CupboardSerializer(many=True)
    kitchenAppliances = KitchenApplianceSerializer(many=True)

    class Meta:
        model = Room
        fields = [
            'makeDefaultRoom', 'roomType', 'name', 'notes', 'photo',
            'doors', 'windows', 'ceilings', 'floors', 'walls',
            'fixturesFittings', 'furnishing', 'cupboard', 'kitchenAppliances'
        ]

class InspectionReportSerializer(WritableNestedModelSerializer):
    propertyDetails = PropertyDetailsSerializer()
    cleaningStandard = CleaningStandardSerializer()
    externalSurfaceType = ExternalSurfaceTypeSerializer(many=True)
    externalFeatures = ExternalFeatureSerializer(many=True)
    boundary = BoundarySerializer(many=True)
    rooms = RoomSerializer(many=True)

    class Meta:
        model  = InspectionReport
        fields = [ 'propertyDetails', 'cleaningStandard', 'inspectedBy',
                   'externalSurfaceType', 'externalFeatures', 'boundary', 'rooms' ]

    def update(self, instance, validated_data):
        # 1) Remove all old nested objects
        #    (one-to-one relations get overwritten; lists we must delete)
        pd = instance.propertyDetails
        pd.tenantDetails.all().delete()
        pd.smokeDetector.all().delete()
        pd.coDetector.all().delete()
        pd.keys.all().delete()
        pd.documents.all().delete()
        # if you have detectors or photos stored elsewhere, clear them too…

        instance.externalSurfaceType.all().delete()
        instance.externalFeatures.all().delete()
        instance.boundary.all().delete()

        for room in instance.rooms.all():
            room.doors.all().delete()
            room.windows.all().delete()
            room.ceilings.all().delete()
            room.floors.all().delete()
            room.walls.all().delete()
            room.fixturesFittings.all().delete()
            room.furnishing.all().delete()
            room.cupboard.all().delete()
            room.kitchenAppliances.all().delete()
        instance.rooms.all().delete()

        # 2) Delegate to writable-nested to re-create everything
        return super().update(instance, validated_data)
