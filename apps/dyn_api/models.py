from django.db import models


# ----------- MAIN PROPERTY DETAILS -----------

class Property(models.Model):
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20)
    property_type = models.CharField(max_length=50)
    detachment = models.CharField(max_length=50)
    front_elevation_photos = models.JSONField(default=list)  # List of URLs
    other_views = models.JSONField(default=list)

    def __str__(self):
        return f"{self.address} ({self.property_type})"


# ----------- TENANTS -----------

class Tenant(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="tenants")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ----------- UTILITIES -----------

class Utility(models.Model):
    UTILITY_CHOICES = [
        ("Gas", "Gas"),
        ("Electricity", "Electricity"),
        ("Water", "Water"),
        ("Heat", "Heat"),
        ("Other", "Other"),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="utilities")
    type = models.CharField(max_length=20, choices=UTILITY_CHOICES)
    reading = models.DecimalField(max_digits=10, decimal_places=2)
    serial_number = models.CharField(max_length=50)
    photo_url = models.URLField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.type} - {self.property.address}"


# ----------- DETECTOR COMPLIANCE -----------

class DetectorCompliance(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="detector_compliance")
    detector_compliance = models.BooleanField()
    solid_fuel_device = models.BooleanField()


# ----------- DETECTORS -----------

class Detector(models.Model):
    DETECTOR_TYPE_CHOICES = [("Smoke", "Smoke"), ("CO", "CO")]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="detectors")
    type = models.CharField(max_length=10, choices=DETECTOR_TYPE_CHOICES)
    working = models.BooleanField()
    location = models.CharField(max_length=100)
    notes = models.TextField(blank=True)


# ----------- KEYS -----------

class Key(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="keys")
    description = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


# ----------- DOCUMENTS -----------

class Document(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="documents")
    description = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


# ----------- CLEANING STANDARD -----------

class CleaningStandard(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="cleaning_standard")
    standard = models.CharField(max_length=50)
    notes = models.TextField(blank=True)


# ----------- INSPECTORS -----------

class Inspector(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inspectors")
    name = models.CharField(max_length=100)


# ----------- EXTERNAL SURFACE -----------

class ExternalSurface(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="external_surfaces")
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


# ----------- EXTERNAL FEATURES -----------

class ExternalFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="external_features")
    feature = models.CharField(max_length=100)
    condition = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


# ----------- BOUNDARY -----------

class Boundary(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="boundaries")
    type = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


# ----------- ROOMS -----------

class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=100)  # e.g., "Main Living Room"
    notes = models.TextField(blank=True)
    photo_url = models.URLField(blank=True, null=True)


# ----------- ROOM SUB-ENTITIES -----------

class Door(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="doors")
    type = models.CharField(max_length=50)
    finish = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    frame_type = models.CharField(max_length=50)
    frame_colour = models.CharField(max_length=50)
    features = models.CharField(max_length=255)
    condition = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


class Window(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="windows")
    type = models.CharField(max_length=50)
    glass_type = models.CharField(max_length=50)
    frame_type = models.CharField(max_length=50)
    frame_colour = models.CharField(max_length=50)
    sill_type = models.CharField(max_length=50)
    sill_colour = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    features = models.CharField(max_length=255)
    openers = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


class Ceiling(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="ceilings")
    finish = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    fittings = models.CharField(max_length=255)
    recessed_spotlights = models.PositiveIntegerField()
    bulbs_not_working = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


class Floor(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="floors")
    finish = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    additions = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


class Wall(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="walls")
    description = models.CharField(max_length=255)
    colour = models.CharField(max_length=50)
    skirting_type = models.CharField(max_length=50)
    skirting_colour = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    features = models.CharField(max_length=255)
    sign_of_leakages = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


class FixtureFitting(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="fixtures_fittings")
    fixture = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    light_switches = models.PositiveIntegerField(default=0)
    plug_sockets = models.PositiveIntegerField(default=0)
    radiators = models.PositiveIntegerField(default=0)
    light_fittings = models.PositiveIntegerField(default=0)
    light_tested = models.BooleanField(default=False)
    plug_sockets_tested = models.BooleanField(default=False)
    electric_switches_safe = models.BooleanField(default=False)
    plug_sockets_safe = models.BooleanField(default=False)
    toilets = models.PositiveIntegerField(default=0)
    basins = models.PositiveIntegerField(default=0)
    base_unit_doors = models.PositiveIntegerField(default=0)
    wall_units = models.PositiveIntegerField(default=0)
    worktops = models.PositiveIntegerField(default=0)
    photo_url = models.URLField()


class Furnishing(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="furnishings")
    furnishings = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


class Cupboard(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="cupboards")
    contents = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()


class KitchenAppliance(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="kitchen_appliances")
    appliances = models.CharField(max_length=255)
    brand = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    tested = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    photo_url = models.URLField()

