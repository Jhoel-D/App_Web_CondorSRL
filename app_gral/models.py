from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, post_save, post_delete

from django.dispatch import receiver

        
class Usuario(AbstractUser):
    CI = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15)
    domicilio = models.TextField()
    fecha_de_registro = models.DateTimeField(auto_now_add=True)
    imagen_perfil = models.ImageField(upload_to='bd_images/', verbose_name='Imagen de perfil', null=True, blank=True)
    def get_status(self):
        return "Activo" if self.is_active else "Dado de baja"
    def __str__(self):
        return self.username

    # Eliminar la imagen asociada al eliminar el usuario
    def delete(self, using=None, keep_parents=False):
        if self.imagen_perfil:
            self.imagen_perfil.storage.delete(self.imagen_perfil.name)
        super().delete(using, keep_parents)

    # Validaciones para la imagen
    def clean(self):
        super().clean()
        if self.imagen_perfil:
            # Validar tamaño máximo (por ejemplo, 5 MB)
            max_size = 5 * 1024 * 1024  # 5 MB
            if self.imagen_perfil.size > max_size:
                raise ValidationError("El tamaño de la imagen no puede exceder los 5 MB.")
            # Validar extensión del archivo
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            if not self.imagen_perfil.name.split('.')[-1].lower() in valid_extensions:
                raise ValidationError("El formato de la imagen debe ser JPG, JPEG, PNG o GIF.")

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def get_status(self):
        return "Activo" if self.is_active else "Dado de baja"

    def __str__(self):
        return self.nombre
class ProductoInventario(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    caracteristicas = models.TextField()
    cantidad_stock = models.PositiveIntegerField(default=0)
    imagen_producto = models.ImageField(upload_to='bd_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def get_status(self):
        return "Activo" if self.is_active else "Dado de baja"
    
    def clean(self):
        if self.precio_unitario < 0:
            raise ValidationError("El precio unitario no puede ser negativo.")
        if self.cantidad_stock < 0:
            raise ValidationError("La cantidad en stock no puede ser negativa.")

    def __str__(self):
        return self.nombre
class IngresoProducto(models.Model):
    id_ingreso = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad de ingreso debe ser mayor a cero.")
    def __str__(self):
        return f"Ingreso de {self.cantidad} {self.id_producto.nombre}"
#MOD VENTAS
class ProductosVenta(models.Model):
    venta = models.ForeignKey('Ventas', on_delete=models.CASCADE, related_name='detalle_productos')
    producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def clean(self):
        # Obtener la instancia previa si existe
        if self.pk:
           instancia_original = ProductosVenta.objects.get(pk=self.pk)
           diferencia_cantidad = self.cantidad - instancia_original.cantidad
        else:
            diferencia_cantidad = self.cantidad
        # Verificar que haya suficiente stock
        if diferencia_cantidad > self.producto.cantidad_stock:
           raise ValidationError(f"La cantidad supera el stock disponible del producto {self.producto.nombre}. El Stock actual es {self.producto.cantidad_stock}.")
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        # Si la instancia ya existe, revertir el stock antes de actualizar
        if self.pk:
            instancia_original = ProductosVenta.objects.get(pk=self.pk)
            diferencia_cantidad = self.cantidad - instancia_original.cantidad
            self.producto.cantidad_stock -= diferencia_cantidad
        else:
            # Reducir el stock al crear una nueva instancia
            self.producto.cantidad_stock -= self.cantidad

        # Verificar que el stock no sea negativo
        if self.producto.cantidad_stock < 0:
            raise ValidationError(f"Stock insuficiente para el producto {self.producto.nombre}.")

        # Guardar el producto actualizado y luego la instancia
        self.producto.save()
        # Calcular el subtotal
        self.subtotal = self.cantidad * self.producto.precio_unitario
        super().save(*args, **kwargs)
    
    @transaction.atomic
    def delete(self, *args, **kwargs):
        # Devolver el stock del producto al eliminar un registro
        self.producto.cantidad_stock += self.cantidad
        self.producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en venta {self.venta.id_venta}"

class Ventas(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
    ]
    id_venta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='ventas_como_cliente')
    id_vendedor = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='ventas_como_vendedor')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    is_active = models.BooleanField(default=True)

    def calcular_costo_total(self):
        # Calcular el costo total sumando los subtotales de los productos
        return sum(item.subtotal for item in self.detalle_productos.all())
    # @transaction.atomic
    # def save(self, *args, **kwargs):
    #     # Guardar la instancia para asignarle un ID si no lo tiene
    #     if not self.pk:
    #         super().save(*args, **kwargs)  # Guardado inicial

    #     # Calcular el costo total y actualizar el campo
    #     self.costo_total = self.calcular_costo_total()
    #     super().save(update_fields=['costo_total'])  # Guardar el costo total actualizado
    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk:  # Si la venta ya existe, recalcula el costo total solo si los productos cambian
            self.costo_total = self.calcular_costo_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta {self.id_venta} - Cliente: {self.id_cliente.username}"

class CarritoItems(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Carrito {self.id_carrito} - {self.id_producto.nombre}"

    @property
    def total_producto(self):
        """Calcula el total de un producto específico (cantidad * precio)."""
        return self.id_producto.precio_unitario * self.cantidad

    @classmethod
    def total_carrito(cls, cliente):
        """Calcula el total del carrito de un cliente específico."""
        return sum(item.total_producto for item in cls.objects.filter(id_cliente=cliente))

#MOD PEDIDOS
class ProductosPedido(models.Model):
    pedido = models.ForeignKey('Pedidos', on_delete=models.CASCADE, related_name='detalle_productos_pedidos')
    producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    

    def clean(self):
        # Obtener la instancia previa si existe
        if self.pk:
           instancia_original = ProductosPedido.objects.get(pk=self.pk)
           diferencia_cantidad = self.cantidad - instancia_original.cantidad
        else:
            diferencia_cantidad = self.cantidad
        # Verificar que haya suficiente stock
        if diferencia_cantidad > self.producto.cantidad_stock:
           raise ValidationError(f"La cantidad supera el stock disponible del producto {self.producto.nombre}. El Stock actual es {self.producto.cantidad_stock}.")
    @transaction.atomic
    def save(self, *args, **kwargs):
        # Si la instancia ya existe, revertir el stock antes de actualizar
        if self.pk:
            instancia_original = ProductosPedido.objects.get(pk=self.pk)
            diferencia_cantidad = self.cantidad - instancia_original.cantidad
            self.producto.cantidad_stock -= diferencia_cantidad
        else:
            # Reducir el stock al crear una nueva instancia
            self.producto.cantidad_stock -= self.cantidad

        # Verificar que el stock no sea negativo
        if self.producto.cantidad_stock < 0:
            raise ValidationError(f"Stock insuficiente para el producto {self.producto.nombre}.")

        # Guardar el producto actualizado y luego la instancia
        self.producto.save()
        # Calcular el subtotal
        self.subtotal = self.cantidad * self.producto.precio_unitario
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Devolver el stock del producto al eliminar un registro
        self.producto.cantidad_stock += self.cantidad
class Pedidos(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos_como_cliente')
    id_vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos_como_vendedor')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    beneficiario = models.CharField(max_length=100)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    celular_a_comunicar = models.CharField(max_length=15)
    lugar_entrega = models.CharField(max_length=100)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    
    def calcular_costo_total(self):
        # Calcular el costo total sumando los subtotales de los productos
        return sum(item.subtotal for item in self.detalle_productos_pedidos.all())
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        # Guardar la instancia para asignarle un ID si no lo tiene
        if not self.pk:
            super().save(*args, **kwargs)  # Guardado inicial

        # Calcular el costo total y actualizar el campo
        self.costo_total = self.calcular_costo_total()
        super().save(update_fields=['costo_total'])  # Guardar el costo total actualizado

    def __str__(self):
        return f"Pedido {self.id_pedido} - Cliente: {self.id_cliente.username}"


#PARA VENTAS
@transaction.atomic
@receiver(post_save, sender=ProductosVenta)
@receiver(post_delete, sender=ProductosVenta)
def actualizar_costo_total(sender, instance, **kwargs):
    """
    Recalcula el costo total de la venta asociada cada vez que se agrega,
    actualiza o elimina un producto en la venta.
    """
    venta = instance.venta
    venta.calcular_costo_total()
    venta.save()
#PARA PEDIDOS
@transaction.atomic
@receiver(post_save, sender=ProductosPedido)
@receiver(post_delete, sender=ProductosPedido)
def actualizar_costo_total(sender, instance, **kwargs):
    pedido = instance.pedido
    pedido.calcular_costo_total()
    pedido.save()