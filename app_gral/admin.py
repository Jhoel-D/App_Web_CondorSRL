from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Usuario, Ventas, Categoria, ProductoInventario, CarritoItems, IngresoProducto, ProductosPedido, ProductosVenta, Pedidos

# Definir una clase para personalizar la vista del usuario en el admin
#MOD USUARIOS
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

#MOD CATEGORÍAS
admin.site.register(Categoria)

#MOD INVENTARIO
@admin.register(ProductoInventario)
class ProductoInventarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_stock', 'precio_unitario', 'is_active')
    search_fields = ('nombre',)
    list_filter = ('is_active',)
    autocomplete_fields = []

#MOD VENTAS
class ProductosVentaInline(admin.TabularInline):
    model = ProductosVenta
    extra = 1  # Número de filas adicionales vacías para agregar nuevos productos
    fields = ('producto', 'cantidad', 'subtotal')  # Mostrar campos relevantes
    readonly_fields = ('subtotal',)  # No permitir editar el subtotal manualmente
    autocomplete_fields = ['producto']  # Activar autocompletar para el campo producto

@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('id_venta', 'id_cliente', 'id_vendedor', 'estado', 'fecha_registro', 'costo_total')
    readonly_fields = ('costo_total',)
    search_fields = ('id_cliente__username', 'id_vendedor__username')
    list_filter = ('estado', 'fecha_registro')
    autocomplete_fields = ['id_cliente', 'id_vendedor']
    inlines = [ProductosVentaInline]

    def save_model(self, request, obj, form, change):
        # No recalcular el costo total aquí, ya que lo maneja el modelo
        super().save_model(request, obj, form, change)

        
#MOD PEDIDOS
class ProductosPedidoInline(admin.TabularInline):
    model = ProductosPedido
    extra = 1  # Número de filas adicionales vacías para agregar nuevos productos
    fields = ('producto', 'cantidad', 'subtotal')  # Mostrar campos relevantes
    readonly_fields = ('subtotal',)  # No permitir editar el subtotal manualmente
    autocomplete_fields = ['producto']  # Activar autocompletar para el campo producto

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'id_cliente', 'id_vendedor', 'estado', 'fecha_registro','beneficiario','monto_pagado', 'celular_a_comunicar', 'lugar_entrega','costo_total',)
    readonly_fields = ('costo_total',)
    search_fields = ('id_cliente__username', 'id_vendedor__username')
    list_filter = ('estado', 'fecha_registro')
    autocomplete_fields = ['id_cliente', 'id_vendedor']  # Usar nombres correctos de campos
    inlines = [ProductosPedidoInline]  # Permitir agregar productos directamente desde la vista de ventas

    def save_model(self, request, obj, form, change):
        # Calcular costo total automáticamente antes de guardar
        obj.calcular_costo_total()
        super().save_model(request, obj, form, change)

#MOD INGRESOS

@admin.register(IngresoProducto)
class IngresoProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'cantidad', 'fecha_ingreso', 'id_usuario')
    list_filter = ('fecha_ingreso',)

admin.site.register(CarritoItems)