# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InspectionReportViewSet

router = DefaultRouter()
router.register(r'inspection-reports', InspectionReportViewSet, basename='inspectionreport')

urlpatterns = [
    path('', include(router.urls)),
]
