from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Usuario, Ventas, Pedido, Categoria, ProductoInventario, CarritoItems, IngresoProducto, ItemsOrderPedido, ProductosVenta

# Definir una clase para personalizar la vista del usuario en el admin
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'fecha_nacimiento','CI', 'telefono', 'domicilio', 'fecha_de_registro', 'imagen_perfil', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Campos básicos
        ('Información personal', {'fields': ('first_name', 'last_name','email','fecha_nacimiento', 'imagen_perfil', 'CI', 'telefono', 'domicilio')}),  # Información extra
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Agregar 'groups' para asignar grupos
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),  # Fechas de registro
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'email', 'fecha_nacimiento', 'CI', 'telefono', 'domicilio'),
        }),
        ('Permisos', {
            'fields': ('groups',),  # Agregar 'groups' al agregar un usuario
        }),
    )


# Registrar el modelo y la clase personalizada del admin
admin.site.register(Usuario, UsuarioAdmin)
#admin.site.register(ProductoInventario)
admin.site.register(Categoria)
admin.site.register(Ventas)
admin.site.register(Pedido)
admin.site.register(CarritoItems)
#admin.site.register(IngresoProducto)
admin.site.register(ItemsOrderPedido)
admin.site.register(ProductosVenta)

@admin.register(ProductoInventario)
class ProductoInventarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_stock', 'precio_unitario', 'id_categoria')

@admin.register(IngresoProducto)
class IngresoProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'cantidad', 'fecha_ingreso', 'id_usuario')
    list_filter = ('fecha_ingreso',)