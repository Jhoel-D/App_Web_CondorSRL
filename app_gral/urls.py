from django.urls import path 
from . import views
#for img
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.menu_principal, name='menu_principal'),  
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'), 
    path('menu_inicio/', views.menu_inicio, name='menu_inicio'), 
    #Cerrar Sesión
    path('cerrar_sesion/',views.cerrar_sesion, name= 'cerrar_sesion'),
    #MOD USUARIOS
    path('mod_usuarios_home/', views.mod_usuarios_home, name='mod_usuarios_home'),
    path('usuario/<int:usuario_id>/', views.ver_usuario, name='ver_usuario'),
    path('usuario/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuario/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuario/registrar/', views.registrar_usuario, name='registrar_usuario'),
    #MOD CLIENTES
    path('mod_clientes_home/', views.mod_clientes_home, name='mod_clientes_home'),
    path('cliente/<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
    path('cliente/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('cliente/registrar/', views.registrar_cliente, name='registrar_cliente'),
    #MOD ROLES
    path('roles/', views.roles_list, name='roles_list'),
    
    path('roles/agregar/', views.agregar_rol, name='agregar_rol'),
    path('roles/editar/<int:rol_id>/', views.editar_rol, name='editar_rol'),
    
    #MOD VER PERFIL
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/restablecer-contrasena/', views.restablecer_contrasena, name='restablecer_contrasena'),
    
    #MOD PRODUCTOS
    path('mod_productos_home/', views.mod_productos_home, name='mod_productos_home'),
    path('producto/<int:producto_id>/', views.ver_producto, name='ver_producto'),
    path('producto/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/crear/', views.crear_producto, name='crear_producto'),
    #MOD CATEGORIAS
    path('categorias/', views.mod_categorias_home, name='mod_categorias_home'),
    path('categoria/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categoria/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('categoria/crear/', views.crear_categoria, name='crear_categoria'),
    
    #MOD VENTAS
    path('ventas/', views.mod_ventas_home, name='mod_ventas_home'),
    path('ventas/<int:venta_id>/productos/', views.ver_productos_venta, name='ver_productos_venta'),
    path('venta/<int:venta_id>/detalle/', views.ver_detalle_venta, name='ver_detalle_venta'),
    path('ventas/editar/<int:venta_id>/', views.editar_venta, name='editar_venta'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
