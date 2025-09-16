
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('CondorSRL/', include('app_web_linea.urls'), name='CondorSRL'),
    path('', include('app_gral.urls')),
]

