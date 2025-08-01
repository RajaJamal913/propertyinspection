
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
 
   path('api/', include('Inspectionreport.urls')),

    path('', include('apps.pages.urls')),
    path('', include('apps.dyn_dt.urls')),
    path('', include('apps.dyn_api.urls')),
    path('charts/', include('apps.charts.urls')),
    path("admin/", admin.site.urls),
    path("", include('admin_soft.urls')),

    
]
