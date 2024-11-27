from django.urls import path 
from . import views

urlpatterns = [
    path('', views.menu_principal, name='menu_principal'),  
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'), 
    path('menu_inicio/', views.menu_inicio, name='menu_inicio'), 
    #Cerrar Sesión
    path('cerrar_sesion/',views.cerrar_sesion, name= 'cerrar_sesion'),
    #MOD USUARIOS
    path('mod_usuarios_home/', views.mod_usuarios_home, name='mod_usuarios_home'),
    #MOD USUARIOS
    path('mod_clientes_home/', views.mod_clientes_home, name='mod_clientes_home'),
]
