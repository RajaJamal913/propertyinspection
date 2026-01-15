

from django.contrib import admin
from django.urls import include, path
from apps.dyn_api import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'property-reports', views.PropertyViewSet, basename='property-reports')

urlpatterns = [
path('api/', views.index, name="dynamic_api"),
path('api/str:model_name/', views.DynamicAPI.as_view(), name="model_api"),
path('api/str:model_name/str:id', views.DynamicAPI.as_view()),
path('api/str:model_name/str:id/', views.DynamicAPI.as_view()),
 path('properties/<int:pk>/report/', views.property_report, name='property_report'),
 path('properties/reports/', views.property_list, name='property_list'),
path('api/', include(router.urls)), # Include router-generated routes
]
