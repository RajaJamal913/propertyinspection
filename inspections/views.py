# inspections/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Inspection
from .serializers import InspectionSerializer

class InspectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows inspections to be viewed or created.
    """
    queryset = Inspection.objects.all().order_by("-created_at")
    serializer_class = InspectionSerializer

