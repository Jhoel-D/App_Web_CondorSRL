
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_gral.urls')),
    path('tienda/', include('app_web_linea.urls')),
]

