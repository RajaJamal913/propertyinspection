# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InspectionReport
from .serializers import InspectionReportSerializer

class InspectionReportViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing inspection reports.
    """
    queryset = InspectionReport.objects.all()
    serializer_class = InspectionReportSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        Custom action to handle bulk creation of inspection reports.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        return Response(serializer.data)

    def perform_bulk_create(self, serializer):
        serializer.save()
