from django.db import models

class PropertyDetails(models.Model):
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    propertyType = models.CharField(max_length=100)
    detachment = models.CharField(max_length=100)
    frontElevationPhoto = models.JSONField(default=list, blank=True)
    otherViews = models.JSONField(default=list, blank=True)
    inspectedBy = models.CharField(max_length=255, blank=True)

class TenantDetail(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, related_name='tenantDetails', on_delete=models.CASCADE)
    tenantName = models.CharField(max_length=255, blank=True)
    tenantEmail = models.EmailField(blank=True)
    mobilePhone = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

class Utilities(models.Model):
    propertyDetails = models.OneToOneField(PropertyDetails, related_name='utilitites', on_delete=models.CASCADE)
    gasMeterReading = models.CharField(max_length=50, blank=True)
    gasMeterSerialNumber = models.CharField(max_length=100, blank=True)
    gasMeterPhoto = models.JSONField(default=list, blank=True)
    electricityMeterReading = models.CharField(max_length=50, blank=True)
    electricityMeterSerialNumber = models.CharField(max_length=100, blank=True)
    electricityMeterPhoto = models.JSONField(default=list, blank=True)
    waterMeterReading = models.CharField(max_length=50, blank=True)
    waterMeterSerialNumber = models.CharField(max_length=100, blank=True)
    waterMeterPhoto = models.JSONField(default=list, blank=True)
    heatMeterReading = models.CharField(max_length=50, blank=True)
    heatMeterSerialNumber = models.CharField(max_length=100, blank=True)
    heatMeterPhoto = models.JSONField(default=list, blank=True)
    otherMeterType = models.CharField(max_length=100, blank=True)
    otherMeterReading = models.CharField(max_length=50, blank=True)
    otherMeterSerialNumber = models.CharField(max_length=100, blank=True)
    otherMeterPhoto = models.JSONField(default=list, blank=True)
    stopcokLocation = models.CharField(max_length=255, blank=True)
    stopcokPhoto = models.JSONField(default=list, blank=True)
    fuseboxLocation = models.CharField(max_length=255, blank=True)
    fuseboxPhoto = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)

class DetectorCompliance(models.Model):
    propertyDetails = models.OneToOneField(PropertyDetails, related_name='detectorCompliance', on_delete=models.CASCADE)
    detectorCompliance = models.CharField(max_length=10)
    solidFuelDevice = models.CharField(max_length=10)

class SmokeDetector(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, related_name='smokeDetector', on_delete=models.CASCADE)
    smokeDetector = models.BooleanField()
    working = models.CharField(max_length=50)
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

class CoDetector(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, related_name='coDetector', on_delete=models.CASCADE)
    coDetector = models.BooleanField()
    working = models.CharField(max_length=50)
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

class Key(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, related_name='keys', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class Document(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, related_name='documents', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class CleaningStandard(models.Model):
    propertyDetails = models.OneToOneField(PropertyDetails, related_name='cleaningStandard', on_delete=models.CASCADE)
    cleaningStandard = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

class ExternalSurfaceType(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, related_name='externalSurfaceType', on_delete=models.CASCADE)
    externalSurfaceType = models.JSONField(default=list, blank=True)
    location = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class ExternalFeature(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, related_name='externalFeatures', on_delete=models.CASCADE)
    externalFeatures = models.JSONField(default=list, blank=True)
    condition = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class Boundary(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, related_name='boundary', on_delete=models.CASCADE)
    boundaryType = models.CharField(max_length=100)
    colour = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    quantity = models.IntegerField()
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class Room(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, related_name='rooms', on_delete=models.CASCADE)
    makeDefaultRoom = models.BooleanField(default=False)
    roomType = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class Door(models.Model):
    room = models.ForeignKey(Room, related_name='doors', on_delete=models.CASCADE)
    makeDefaultDoor = models.BooleanField(default=False)
    doorType = models.CharField(max_length=100, blank=True)
    doorFinish = models.CharField(max_length=100, blank=True)
    doorColour = models.CharField(max_length=50, blank=True)
    frameType = models.CharField(max_length=100, blank=True)
    frameColour = models.CharField(max_length=50, blank=True)
    features = models.JSONField(default=list, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class Window(models.Model):
    room = models.ForeignKey(Room, related_name='windows', on_delete=models.CASCADE)
    makeDefaultWindow = models.BooleanField(default=False)
    windowType = models.CharField(max_length=100, blank=True)
    glassType = models.CharField(max_length=100, blank=True)
    frameType = models.CharField(max_length=100, blank=True)
    frameColour = models.CharField(max_length=50, blank=True)
    sillType = models.CharField(max_length=100, blank=True)
    sillColour = models.CharField(max_length=50, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    features = models.JSONField(default=list, blank=True)
    openers = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class Ceiling(models.Model):
    room = models.ForeignKey(Room, related_name='ceilings', on_delete=models.CASCADE)
    makeDefaultCeiling = models.BooleanField(default=False)
    ceilingFinish = models.CharField(max_length=100, blank=True)
    colour = models.CharField(max_length=50, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    ceilingFittings = models.JSONField(default=list, blank=True)
    recessedSpotlights = models.IntegerField(default=0)
    bulbsNotWorking = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class Wall(models.Model):
    room = models.ForeignKey(Room, related_name='walls', on_delete=models.CASCADE)
    makeDefaultWall = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    colour = models.CharField(max_length=50, blank=True)
    skirtingType = models.CharField(max_length=100, blank=True)
    skirtingColour = models.CharField(max_length=50, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    features = models.JSONField(default=list, blank=True)
    signOfLeakages = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class FixtureFitting(models.Model):
    room = models.ForeignKey(Room, related_name='fixturesFittings', on_delete=models.CASCADE)
    fixture = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    lightSwitches = models.IntegerField(default=0)
    plugSockets = models.IntegerField(default=0)
    radiators = models.IntegerField(default=0)
    loghtFittings = models.IntegerField(default=0)
    lightTested = models.BooleanField(default=False)
    plugSocketsTested = models.BooleanField(default=False)
    electricSwitchesVisualluSafe = models.BooleanField(default=False)
    PlugSocketsVisuallySafe = models.BooleanField(default=False)
    toilets = models.IntegerField(default=0)
    basins = models.IntegerField(default=0)
    baseUnitDoors = models.IntegerField(default=0)
    wallUnits = models.IntegerField(default=0)
    worktops = models.IntegerField(default=0)
    photo = models.JSONField(default=list, blank=True)

class Furnishing(models.Model):
    room = models.ForeignKey(Room, related_name='furnishing', on_delete=models.CASCADE)
    furnishing = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)

class Cupboard(models.Model):
    room = models.ForeignKey(Room, related_name='cupboard', on_delete=models.CASCADE)
    cupboardContent = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list, blank=True)
