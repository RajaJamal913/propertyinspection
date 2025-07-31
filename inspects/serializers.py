from rest_framework import serializers
from .models import (
    PropertyDetails, TenantDetail, Utilities, DetectorCompliance,
    SmokeDetector, CoDetector, Key, Document, CleaningStandard,
    ExternalSurfaceType, ExternalFeature, Boundary, Room,
    Door, Window, Ceiling, Wall, FixtureFitting, Furnishing, Cupboard
)

class TenantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantDetail
        fields = ['tenantName', 'tenantEmail', 'mobilePhone', 'notes']

class UtilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilities
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

class CoDetectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoDetector
        fields = ['coDetector', 'working', 'location', 'notes']

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ['description', 'notes', 'photo']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['description', 'notes', 'photo']

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
        fields = ['makeDefaultDoor', 'doorType', 'doorFinish', 'doorColour', 'frameType', 'frameColour', 'features', 'condition', 'notes', 'photo']

class WindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Window
        fields = ['makeDefaultWindow', 'windowType', 'glassType', 'frameType', 'frameColour', 'sillType', 'sillColour', 'condition', 'features', 'openers', 'notes', 'photo']

class CeilingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceiling
        fields = ['makeDefaultCeiling', 'ceilingFinish', 'colour', 'condition', 'ceilingFittings', 'recessedSpotlights', 'bulbsNotWorking', 'notes', 'photo']

class WallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wall
        fields = ['makeDefaultWall', 'description', 'colour', 'skirtingType', 'skirtingColour', 'condition', 'features', 'signOfLeakages', 'notes', 'photo']

class FixtureFittingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixtureFitting
        fields = [
            'fixture', 'notes', 'lightSwitches', 'plugSockets', 'radiators', 'loghtFittings',
            'lightTested', 'plugSocketsTested', 'electricSwitchesVisualluSafe', 'PlugSocketsVisuallySafe',
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

class RoomSerializer(serializers.ModelSerializer):
    doors = DoorSerializer(many=True)
    windows = WindowSerializer(many=True)
    ceilings = CeilingSerializer(many=True)
    walls = WallSerializer(many=True)
    fixturesFittings = FixtureFittingSerializer(many=True)
    furnishing = FurnishingSerializer(many=True)
    cupboard = CupboardSerializer(many=True)

    class Meta:
        model = Room
        fields = ['makeDefaultRoom', 'roomType', 'name', 'notes', 'photo', 'doors', 'windows', 'ceilings', 'walls', 'fixturesFittings', 'furnishing', 'cupboard']

class PropertyDetailsSerializer(serializers.ModelSerializer):
    tenantDetails = TenantDetailSerializer(many=True)
    utilitites = UtilitiesSerializer()
    detectorCompliance = DetectorComplianceSerializer()
    smokeDetector = SmokeDetectorSerializer(many=True)
    coDetector = CoDetectorSerializer(many=True)
    keys = KeySerializer(many=True)
    documents = DocumentSerializer(many=True)
    cleaningStandard = CleaningStandardSerializer()
    externalSurfaceType = ExternalSurfaceTypeSerializer(many=True)
    externalFeatures = ExternalFeatureSerializer(many=True)
    boundary = BoundarySerializer(many=True)
    rooms = RoomSerializer(many=True)

    class Meta:
        model = PropertyDetails
        fields = [
            'address', 'postcode', 'propertyType', 'detachment', 'frontElevationPhoto', 'otherViews', 'inspectedBy',
            'tenantDetails', 'utilitites', 'detectorCompliance', 'smokeDetector', 'coDetector', 'keys', 'documents',
            'cleaningStandard', 'externalSurfaceType', 'externalFeatures', 'boundary', 'rooms'
        ]

    def create(self, validated_data):
        tenants = validated_data.pop('tenantDetails')
        utilities_data = validated_data.pop('utilitites')
        detector_data = validated_data.pop('detectorCompliance')
        smoke_data = validated_data.pop('smokeDetector')
        co_data = validated_data.pop('coDetector')
        keys_data = validated_data.pop('keys')
        docs_data = validated_data.pop('documents')
        cleaning_data = validated_data.pop('cleaningStandard')
        ext_surf_data = validated_data.pop('externalSurfaceType')
        ext_feat_data = validated_data.pop('externalFeatures')
        boundary_data = validated_data.pop('boundary')
        rooms_data = validated_data.pop('rooms')

        property_obj = PropertyDetails.objects.create(**validated_data)
        TenantDetail.objects.bulk_create([TenantDetail(propertyDetails=property_obj, **t) for t in tenants])
        Utilities.objects.create(propertyDetails=property_obj, **utilities_data)
        DetectorCompliance.objects.create(propertyDetails=property_obj, **detector_data)
        for s in smoke_data:
            SmokeDetector.objects.create(propertyDetails=property_obj, **s)
        for c in co_data:
            CoDetector.objects.create(propertyDetails=property_obj, **c)
        for k in keys_data:
            Key.objects.create(propertyDetails=property_obj, **k)
        for d in docs_data:
            Document.objects.create(propertyDetails=property_obj, **d)
        CleaningStandard.objects.create(propertyDetails=property_obj, **cleaning_data)
        for es in ext_surf_data:
            ExternalSurfaceType.objects.create(propertyDetails=property_obj, **es)
        for ef in ext_feat_data:
            ExternalFeature.objects.create(propertyDetails=property_obj, **ef)
        for b in boundary_data:
            Boundary.objects.create(propertyDetails=property_obj, **b)
        
        for room in rooms_data:
            doors = room.pop('doors')
            windows = room.pop('windows')
            ceilings = room.pop('ceilings')
            walls = room.pop('walls')
            fixtures = room.pop('fixturesFittings')
            furnishing = room.pop('furnishing')
            cupboard = room.pop('cupboard')

            room_obj = Room.objects.create(propertyDetails=property_obj, **room)
            Door.objects.bulk_create([Door(room=room_obj, **d) for d in doors])
            Window.objects.bulk_create([Window(room=room_obj, **w) for w in windows])
            Ceiling.objects.bulk_create([Ceiling(room=room_obj, **c) for c in ceilings])
            Wall.objects.bulk_create([Wall(room=room_obj, **w) for w in walls])
            FixtureFitting.objects.bulk_create([FixtureFitting(room=room_obj, **f) for f in fixtures])
            Furnishing.objects.bulk_create([Furnishing(room=room_obj, **f) for f in furnishing])
            Cupboard.objects.bulk_create([Cupboard(room=room_obj, **c) for c in cupboard])

        return property_obj
