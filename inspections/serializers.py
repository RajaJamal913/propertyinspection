# inspections/serializers.py
from rest_framework import serializers
from .models import Inspection

class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = [
            "id",
            "property_details",
            "cleaning_standard",
            "inspected_by",
            "external_surface_type",
            "external_features",
            "boundary",
            "rooms",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
