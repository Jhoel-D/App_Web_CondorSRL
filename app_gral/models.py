from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete

        
class Usuario(AbstractUser):
    CI = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15)
    domicilio = models.TextField()
    fecha_de_registro = models.DateTimeField(auto_now_add=True)
    imagen_perfil = models.ImageField(upload_to='bd_images/', verbose_name='Imagen de perfil', null=True, blank=True)

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

class ProductosVenta(models.Model):
    id_venta_detalle = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.cantidad > self.id_producto.cantidad_stock:
            raise ValidationError("La cantidad supera el stock disponible del producto.")
    def __str__(self):
        return f"Detalle Venta  {self.id_producto.nombre}"
class Ventas(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
    BOLIVIAN_DEPARTMENTS = [
        ('LP', 'La Paz'),
        ('CBB', 'Cochabamba'),
        ('SCZ', 'Santa Cruz'),
        ('OR', 'Oruro'),
        ('PT', 'Potosí'),
        ('TJ', 'Tarija'),
        ('CH', 'Chuquisaca'),
        ('BE', 'Beni'),
        ('PD', 'Pando'),
        ('El Alto', 'El Alto'),
    ]
    id_venta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='ventas_como_cliente'
    )
    id_vendedor = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='ventas_como_vendedor'
    )
    productos_de_venta = models.ManyToManyField(ProductosVenta, related_name='ventas', blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    departamento = models.CharField(max_length=100, choices=BOLIVIAN_DEPARTMENTS, default='')

    def save(self, *args, **kwargs):
        # Solo guarda el objeto sin calcular costo_total la primera vez
        if not self.pk:
            super().save(*args, **kwargs)

        # Calcula el costo_total después de que la instancia tenga un ID
        self.costo_total = sum(
            item.id_producto.precio_unitario * item.cantidad 
            for item in self.productos_de_venta.all()
        )
        super().save(*args, **kwargs)  # Guarda nuevamente con costo_total actualizado

    def __str__(self):
        return f"Venta {self.id_venta} - {self.id_cliente.username}"

    
class CarritoItems(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_añadida = models.DateTimeField(auto_now_add=True)

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

class ItemsOrderPedido(models.Model): #ItemsOrder
    id_carrito = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_añadida = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Carrito {self.id_carrito} - {self.id_producto.nombre}"
    
class Pedido(models.Model):  # Orden
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
    BOLIVIAN_DEPARTMENTS = [
        ('LP', 'La Paz'),
        ('CBB', 'Cochabamba'),
        ('SCZ', 'Santa Cruz'),
        ('OR', 'Oruro'),
        ('PT', 'Potosí'),
        ('TJ', 'Tarija'),
        ('CH', 'Chuquisaca'),
        ('BE', 'Beni'),
        ('PD', 'Pando'),
        ('El Alto', 'El Alto'),
    ]
    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    productos_en_pedido = models.ManyToManyField(ItemsOrderPedido, related_name='orders', blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    departamento = models.CharField(max_length=100, choices=BOLIVIAN_DEPARTMENTS, default='')
    celular_a_comunicar = models.CharField(max_length=15)
    lugar_entrega = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Guarda la instancia por primera vez para asignar un ID
        if not self.pk:
            super().save(*args, **kwargs)

        # Calcula el monto total sumando (precio_unitario * cantidad) de cada producto en el pedido
        self.monto_total = sum(
            item.id_producto.precio_unitario * item.cantidad
            for item in self.productos_en_pedido.all()
        )
        # Guarda nuevamente con el monto total actualizado
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.id_cliente.username}"
