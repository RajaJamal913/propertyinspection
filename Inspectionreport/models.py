from django.db import models
from django.db import models


class InspectionReport(models.Model):
    inspectedBy = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Inspection by {self.inspectedBy} (#{self.pk})"


class PropertyDetails(models.Model):
    report = models.OneToOneField(InspectionReport, on_delete=models.CASCADE, related_name="propertyDetails")
    address = models.CharField(max_length=500, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    propertyType = models.CharField(max_length=100, blank=True)
    detachment = models.CharField(max_length=100, blank=True)
    frontElevationPhoto = models.JSONField(default=list)
    otherViews = models.JSONField(default=list)

    def __str__(self):
        return f"Property @ {self.address}"


class TenantDetail(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, on_delete=models.CASCADE, related_name="tenantDetails")
    tenantName = models.CharField(max_length=255, blank=True)
    tenantEmail = models.EmailField(blank=True)
    mobilePhone = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)


class Utility(models.Model):
    propertyDetails = models.OneToOneField(PropertyDetails, on_delete=models.CASCADE, related_name="utilitites")
    gasMeterReading = models.CharField(max_length=100, blank=True)
    gasMeterSerialNumber = models.CharField(max_length=100, blank=True)
    gasMeterPhoto = models.JSONField(default=list)

    electricityMeterReading = models.CharField(max_length=100, blank=True)
    electricityMeterSerialNumber = models.CharField(max_length=100, blank=True)
    electricityMeterPhoto = models.JSONField(default=list)

    waterMeterReading = models.CharField(max_length=100, blank=True)
    waterMeterSerialNumber = models.CharField(max_length=100, blank=True)
    waterMeterPhoto = models.JSONField(default=list)

    heatMeterReading = models.CharField(max_length=100, blank=True)
    heatMeterSerialNumber = models.CharField(max_length=100, blank=True)
    heatMeterPhoto = models.JSONField(default=list)

    otherMeterType = models.CharField(max_length=100, blank=True)
    otherMeterReading = models.CharField(max_length=100, blank=True)
    otherMeterSerialNumber = models.CharField(max_length=100, blank=True)
    otherMeterPhoto = models.JSONField(default=list)

    stopcokLocation = models.CharField(max_length=255, blank=True)
    stopcokPhoto = models.JSONField(default=list)

    fuseboxLocation = models.CharField(max_length=255, blank=True)
    fuseboxPhoto = models.JSONField(default=list)

    notes = models.TextField(blank=True)


class DetectorCompliance(models.Model):
    propertyDetails = models.OneToOneField(PropertyDetails, on_delete=models.CASCADE, related_name="detectorCompliance")
    detectorCompliance = models.CharField(max_length=3, choices=[("YES","YES"),("NO","NO")])
    solidFuelDevice = models.CharField(max_length=3, choices=[("YES","YES"),("NO","NO")])


class SmokeDetector(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, on_delete=models.CASCADE, related_name="smokeDetector")
    smokeDetector = models.BooleanField(default=False)
    working = models.CharField(max_length=50, choices=[("Working","Working"),("Not Working","Not Working")])
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)


class CODetector(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, on_delete=models.CASCADE, related_name="coDetector")
    coDetector = models.BooleanField(default=False)
    working = models.CharField(max_length=50, choices=[("Working","Working"),("Not Working","Not Working")])
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)


class Key(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, on_delete=models.CASCADE, related_name="keys")
    description = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class Document(models.Model):
    propertyDetails = models.ForeignKey(PropertyDetails, on_delete=models.CASCADE, related_name="documents")
    description = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class CleaningStandard(models.Model):
    report = models.OneToOneField(InspectionReport, on_delete=models.CASCADE, related_name="cleaningStandard")
    cleaningStandard = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)


class ExternalSurfaceType(models.Model):
    report = models.ForeignKey(InspectionReport, on_delete=models.CASCADE, related_name="externalSurfaceType")
    externalSurfaceType = models.JSONField(default=list)
    location = models.JSONField(default=list)   # e.g. ["Back","Front","Side"]
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class ExternalFeature(models.Model):
    report = models.ForeignKey(InspectionReport, on_delete=models.CASCADE, related_name="externalFeatures")
    externalFeatures = models.JSONField(default=list)
    condition = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class Boundary(models.Model):
    report = models.ForeignKey(InspectionReport, on_delete=models.CASCADE, related_name="boundary")
    boundaryType = models.CharField(max_length=100, blank=True)
    colour = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class Room(models.Model):
    report = models.ForeignKey(InspectionReport, on_delete=models.CASCADE, related_name="rooms")
    makeDefaultRoom = models.BooleanField(default=False)
    roomType = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class Door(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="doors")
    makeDefaultDoor = models.BooleanField(default=False)
    doorType = models.CharField(max_length=100, blank=True)
    doorFinish = models.CharField(max_length=100, blank=True)
    doorColour = models.CharField(max_length=100, blank=True)
    frameType = models.CharField(max_length=100, blank=True)
    frameColour = models.CharField(max_length=100, blank=True)
    features = models.JSONField(default=list)
    condition = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class Window(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="windows")
    makeDefaultWindow = models.BooleanField(default=False)
    windowType = models.CharField(max_length=100, blank=True)
    glassType = models.CharField(max_length=100, blank=True)
    frameType = models.CharField(max_length=100, blank=True)
    frameColour = models.CharField(max_length=100, blank=True)
    sillType = models.CharField(max_length=100, blank=True)
    sillColour = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    features = models.JSONField(default=list)
    openers = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class Ceiling(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="ceilings")
    makeDefaultCeiling = models.BooleanField(default=False)
    ceilingFinish = models.CharField(max_length=100, blank=True)
    colour = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    ceilingFittings = models.JSONField(default=list)
    recessedSpotlights = models.IntegerField(default=0)
    bulbsNotWorking = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class Floor(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="floors")
    makeDefaultFloor = models.BooleanField(default=False)
    floorFinish = models.CharField(max_length=100, blank=True)
    colour = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    additions = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class Wall(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="walls")
    makeDefaultWall = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    colour = models.CharField(max_length=100, blank=True)
    skirtingType = models.CharField(max_length=100, blank=True)
    skirtingColour = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    features = models.JSONField(default=list)
    signOfLeakages = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class FixtureFitting(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="fixturesFittings")
    fixture = models.JSONField(default=list)
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
    photo = models.JSONField(default=list)


class Furnishing(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="furnishing")
    furnishing =models.JSONField(default=list)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class Cupboard(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="cupboard")
    cupboardContent = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)


class KitchenAppliance(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="kitchenAppliances")
    kitchenAppliances = models.JSONField(default=list)
    brand = models.CharField(max_length=100, blank=True)
    colour = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(default=0)
    tested = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    photo = models.JSONField(default=list)
