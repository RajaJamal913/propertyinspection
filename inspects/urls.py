from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PropertyDetailsViewSet

router = DefaultRouter()
router.register(r'property-details', PropertyDetailsViewSet, basename='propertydetails')

urlpatterns = [
    path('', include(router.urls)),
]
