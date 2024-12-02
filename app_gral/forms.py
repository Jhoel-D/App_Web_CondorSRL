from django import forms
from django.contrib.auth.models import User, Group

from .models import Usuario, ProductoInventario, Categoria

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


from django import forms
from django.contrib.auth.models import Group
from .models import Usuario  # Asegúrate de importar el modelo correcto

class UsuarioCreateForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.exclude(name="Cliente"),  # Excluye el grupo "Cliente"
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
            if grupo:
                usuario.groups.add(grupo)  # Asocia el grupo al usuario
        return usuario

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
