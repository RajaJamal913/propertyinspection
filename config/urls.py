
from django.contrib import admin
from django.urls import include, path
import nested_admin

urlpatterns = [

    path('', include('apps.pages.urls')),
    path('', include('apps.dyn_dt.urls')),
    path('', include('apps.dyn_api.urls')),
    path('charts/', include('apps.charts.urls')),
    path("admin/", admin.site.urls),
    path("", include('admin_soft.urls')),
    path('_nested_admin/', include('nested_admin.urls')),

    
]
