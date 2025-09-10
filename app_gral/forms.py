from django import forms
from django.contrib.auth.models import User, Group

from .models import Usuario, ProductoInventario, Categoria, Usuario, Ventas, ProductosVenta, Pedidos, ProductosPedido, Cliente

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telefono', 'domicilio', 'fecha_nacimiento', 'imagen_perfil']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        
    telefono = forms.CharField(max_length=15, required=False)
    domicilio = forms.CharField(max_length=255, required=False)
    fecha_nacimiento = forms.DateField(required=False)
    imagen_perfil = forms.ImageField(required=False)

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'CI', 'fecha_nacimiento', 'telefono', 'domicilio', 'domicilio', 'imagen_perfil']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['CI', 'nombre', 'apellido', 'telefono', 'direccion', 'email', 'fecha_nacimiento']


class UsuarioCreateForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(), # Excluye el grupo "Cliente"
        required=False,
        label="Grupo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'telefono', 'CI', 'domicilio', 'fecha_nacimiento', 'imagen_perfil']
        widgets = {
            'CI': forms.NumberInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-select'}),
            'imagen_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])  # Encripta la contraseña
        if commit:
            usuario.save()
            grupo = self.cleaned_data.get('grupo')  # Obtén el grupo seleccionado
            if not grupo:  # Si no se selecciona ningún grupo
                try:
                    grupo = Group.objects.get(name="Cliente")  # Busca el grupo "Cliente"
                except Group.DoesNotExist:
                    raise ValueError("El grupo 'Cliente' no existe. Por favor, créalo en el sistema.")  
            usuario.groups.add(grupo)  # Asocia el grupo (seleccionado o predeterminado) al usuario
        return usuario

class ClienteCreateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['CI', 'nombre', 'apellido', 'telefono', 'direccion', 'email', 'fecha_nacimiento']
        widgets = {
            'CI': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-select'}),
        }

class ProductoInventarioForm(forms.ModelForm):
    class Meta:
        model = ProductoInventario
        fields = ['nombre', 'descripcion', 'precio_unitario', 'cantidad_stock', 'imagen_producto', 'id_categoria', 'caracteristicas']



    def clean_cantidad_stock(self):
        cantidad = self.cleaned_data.get('cantidad_stock')
        if cantidad < 0:
            raise forms.ValidationError('La cantidad en stock no puede ser negativa.')
        return cantidad
    

class ProductoInventarioCreateForm(forms.ModelForm):
    class Meta:
        model = ProductoInventario
        fields = ['nombre', 'descripcion', 'precio_unitario', 'cantidad_stock', 'imagen_producto', 'id_categoria', 'caracteristicas']
    widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen_producto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_categoria': forms.Select(attrs={'class': 'form-select'}),
            'caracteristicas': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar categorías activas
        self.fields['id_categoria'].queryset = Categoria.objects.filter(is_active=True)
        # Establecer valores predeterminados como vacíos si es necesario
        if not self.instance.pk:
            self.fields['id_categoria'].empty_label = "Seleccione una categoría"  # Asegura que no haya valor seleccionado por defecto
    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_cantidad_stock(self):
        cantidad = self.cleaned_data.get('cantidad_stock')
        if cantidad < 0:
            raise forms.ValidationError('La cantidad en stock no puede ser negativa.')
        return cantidad


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['id_categoria', 'nombre', 'descripcion']
        

class CategoriaCreateForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['id_categoria', 'nombre', 'descripcion']
    widgets = {
            'id_categoria': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

from django.forms.models import modelformset_factory
from django.contrib import admin
class VentasForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = ['id_cliente', 'costo_total', 'estado']
        widgets = {
            'costo_total': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_cliente'].queryset = Cliente.objects.filter(is_active=True)
    
    

class ProductosVentaForm(forms.ModelForm):
    class Meta:
        model = ProductosVenta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_producto(self):
        producto = self.cleaned_data.get('producto')
        if not producto:
            raise forms.ValidationError("El campo producto no puede estar vacío.")
        return producto


ItemsOrderFormSet = modelformset_factory(
    ProductosVenta,
    form=ProductosVentaForm,
    extra=0,
    can_delete=True
)

class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['id_cliente', 'beneficiario', 'celular_a_comunicar','estado', 'monto_pagado']
        widgets = {
            'costo_total': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        
class ProductosPedidoForm(forms.ModelForm):
    class Meta:
        model = ProductosPedido
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_producto(self):
        producto = self.cleaned_data.get('producto')
        if not producto:
            raise forms.ValidationError("El campo producto no puede estar vacío.")
        return producto


ItemsOrderFormSet = modelformset_factory(
    ProductosPedido,
    form=ProductosPedidoForm,
    extra=0,
    can_delete=True
)
