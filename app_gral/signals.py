from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IngresoProducto, ProductoInventario

@receiver(post_save, sender=IngresoProducto)
def actualizar_stock(sender, instance, created, **kwargs):
    """
    Señal para actualizar el stock del producto cuando se realiza un ingreso.
    """
    if created:  # Solo ejecuta cuando se crea un nuevo ingreso
        producto = instance.id_producto  # Obtener el producto relacionado
        producto.cantidad_stock += instance.cantidad  # Sumar la cantidad ingresada al stock
        producto.save()  # Guardar los cambios en el producto
