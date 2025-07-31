from rest_framework import viewsets
from .models import PropertyDetails
from .serializers import PropertyDetailsSerializer

class PropertyDetailsViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    to create, retrieve, update, and delete PropertyDetails
    along with all nested related data.
    """
    queryset = PropertyDetails.objects.all()
    serializer_class = PropertyDetailsSerializer
