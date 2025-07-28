from django.db import models

# Create your models here.
# inspections/models.py
from django.db import models

class Inspection(models.Model):
    property_details        = models.JSONField()
    cleaning_standard       = models.JSONField()
    inspected_by            = models.CharField(max_length=255)
    external_surface_type   = models.JSONField()
    external_features       = models.JSONField()
    boundary                = models.JSONField()
    rooms                   = models.JSONField()
    created_at              = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection #{self.pk} by {self.inspected_by}"
