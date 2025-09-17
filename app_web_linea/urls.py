from django.urls import path 
from .views import sector_informativo

urlpatterns = [
    path('', sector_informativo, name='sector_informativo'), 
]
