from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reports/manual/pdf/', views.property_manual_pdf, name='property_manual_pdf'),
]
