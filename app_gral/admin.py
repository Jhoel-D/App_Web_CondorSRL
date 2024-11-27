from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Usuario, Ventas, Pedido, Categoria, ProductoInventario

# Definir una clase para personalizar la vista del usuario en el admin
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'birth_date','CI', 'telefono', 'domicilio', 'fecha_de_registro', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Campos básicos
        ('Información personal', {'fields': ('first_name', 'last_name', 'birth_date', 'CI', 'telefono', 'domicilio')}),  # Información extra
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Agregar 'groups' para asignar grupos
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),  # Fechas de registro
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'birth_date', 'CI', 'telefono', 'domicilio'),
        }),
        ('Permisos', {
            'fields': ('groups',),  # Agregar 'groups' al agregar un usuario
        }),
    )

# Registrar el modelo y la clase personalizada del admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(ProductoInventario)
admin.site.register(Categoria)
admin.site.register(Ventas)
admin.site.register(Pedido)