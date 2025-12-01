from django.contrib import admin
from django.urls import path, include
from dashboard.views import index

urlpatterns = [
    path('', index, name='index'),                    
    path('monitoreo/', include('monitoreo.urls')),     
    path('admin/', admin.site.urls),
]
