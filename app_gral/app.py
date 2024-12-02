from django.contrib.auth.models import Group
from django.apps import AppConfig

def crear_grupos():
    admin_group, created = Group.objects.get_or_create(name='Administrador')
    vendedor_group, created = Group.objects.get_or_create(name='Vendedor')
    cliente_group, created = Group.objects.get_or_create(name='Cliente')

# Llama a la función cuando sea necesario


