from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Campos personalizados adicionales
    CI = models.CharField(max_length=20, unique=True, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)  # Fecha de nacimiento
    telefono = models.CharField(max_length=15)
    domicilio = models.TextField()
    fecha_de_registro = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        
        return self.username

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

    def __str__(self):
        return self.nombre
class IngresoProducto(models.Model):
    id_ingreso = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ingreso de {self.cantidad} {self.id_producto.nombre}"
class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id_venta} - {self.id_cliente.username}"
class VentaDetalle(models.Model):
    id_venta_detalle = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Venta {self.id_venta.id_venta} - {self.id_producto.nombre}"
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.id_cliente.username}"
class PedidoDetalle(models.Model):
    id_pedido_detalle = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Detalle Pedido {self.id_pedido.id_pedido} - {self.id_producto.nombre}"
class CarritoItems(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_añadida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito {self.id_carrito} - {self.id_producto.nombre}"
class OrdenCarritoPedido(models.Model):
    id = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_de_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden de Carrito {self.id} - {self.id_producto.nombre}"

