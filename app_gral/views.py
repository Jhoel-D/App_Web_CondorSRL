from django.shortcuts import render,redirect, get_object_or_404

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm #Añadido
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
from .models import Usuario, ProductoInventario
from django.db.models import Q #para or en python
from django.core.paginator import Paginator

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UsuarioUpdateForm, ProductoInventarioForm, ProductoInventarioCreateForm, UsuarioForm, UsuarioCreateForm


# Create your views here.
def menu_principal(request):
    es_administrador = request.user.groups.filter(name='Administrador').exists()
    return render(request, 'menu_principal.html', {'es_administrador': es_administrador})

@login_required  
def menu_inicio(request):
    return render(request, 'menu_inicio.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Crea una instancia del formulario con los datos del POST
        if form.is_valid():  # Verifica si el formulario es válido
            user = form.get_user()  # Obtiene el usuario del formulario
            login(request, user)  # Inicia sesión al usuario
            return redirect('menu_principal')  # Redirige a la vista de cómics y mangas
        else:
            return render(request, 'iniciar_sesion.html', {
                'form': form,
                'error_message': 'Usuario o contraseña incorrectos'
            })
    else:
        form = AuthenticationForm()  # Crea una instancia vacía del formulario
    return render(request, 'iniciar_sesion.html', {'form': form})  # Renderiza la plantilla de inicio de sesión

# Logout o Cerrar Sesión
@login_required
def cerrar_sesion (request):
    logout(request)
    return redirect ('menu_principal')  

#MOD 1 USUARIOS
@login_required
def mod_usuarios_home(request):
    # Obtener el grupo "Cliente"
    grupo_clientes = Group.objects.get(name='Cliente')

    # Excluir usuarios del grupo "Cliente"
    usuarios = Usuario.objects.exclude(groups=grupo_clientes)

    # Filtro de búsqueda
    search_term = request.GET.get('search', '')
    if search_term:
        usuarios = usuarios.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(CI__icontains=search_term) |
            Q(username__icontains=search_term)
        )

    # Paginación
    paginator = Paginator(usuarios, 10)  # Mostrar 8 usuarios por página
    page_number = request.GET.get('page')
    usuarios_page = paginator.get_page(page_number)

    # Renderizar la plantilla con los usuarios paginados
    return render(request, 'usuarios/mod_personal/mod_usuarios_home.html', {
        'usuarios': usuarios_page,
        'search_term': search_term
    })

def ver_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'usuarios/mod_personal/ver_usuario.html', {'usuario': usuario})



def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario editado exitosamente.')
            return redirect('mod_usuarios_home')
        else:
            # Imprimir errores en la consola para depuración
            print(form.errors)
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/mod_personal/editar_usuario.html', {'form': form, 'usuario': usuario})

def eliminar_usuario(request, producto_id):
    producto = get_object_or_404(ProductoInventario, id_producto=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado exitosamente.')
    return redirect('mod_productos_home')

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Esto ya maneja la asociación del grupo en el método save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('mod_usuarios_home')  # Redirige al home o la página deseada
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = UsuarioCreateForm()
    
    return render(request, 'usuarios/mod_personal/registrar_usuario.html', {'form': form})


# MOD CLIENTES
@login_required  
def mod_clientes_home(request):
    grupo_clientes = Group.objects.get(name='Cliente')
    usuarios = Usuario.objects.filter(groups=grupo_clientes)

    # Búsqueda por término
    search_term = request.GET.get('search', '')
    if search_term:
        usuarios = usuarios.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(CI__icontains=search_term)
        )

    # Paginación
    paginator = Paginator(usuarios, 8)  # Mostrar 8 clientes por página
    page_number = request.GET.get('page')
    usuarios_page = paginator.get_page(page_number)

    return render(request, 'usuarios/mod_cliente/mod_clientes_home.html', {
        'usuarios': usuarios_page,
        'search_term': search_term
    })

#MOD ROLES
@login_required
def roles_list(request):
    roles = Group.objects.all()
    return render(request, 'usuarios/mod_personal/roles_list.html', {'roles': roles})

def agregar_rol(request):
    if request.method == 'POST':
        nombre_rol = request.POST.get('nombre_rol')
        if nombre_rol:
            Group.objects.create(name=nombre_rol)
        return redirect('roles_list')
    return render(request, 'usuarios/mod_personal/agregar_rol.html')

#MOD VER PERFIL
@login_required
def ver_perfil(request):
    user = request.user  # Obtenemos al usuario autenticado
    return render(request, 'usuarios/ver_perfil.html', {'user': user})
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Perfil actualizado correctamente!")
            return redirect('ver_perfil')
    else:
        form = UsuarioUpdateForm(instance=request.user)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@login_required
def restablecer_contrasena(request):
    """Vista para restablecer la contraseña del usuario."""
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Mantener sesión activa
            messages.success(request, "¡Contraseña actualizada correctamente!")
            return redirect('ver_perfil')
        else:
            messages.error(request, "Por favor corrige los errores abajo.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'usuarios/restablecer_contraseña.html', {'form': form})

#MOD PRODUCTOS
def mod_productos_home(request):
    search_term = request.GET.get('search', '')
    productos = ProductoInventario.objects.filter(nombre__icontains=search_term)
    
    # Paginación
    paginator = Paginator(productos, 10)  # Muestra 10 productos por página
    page_number = request.GET.get('page')  # Número de página desde la URL
    productos_paginados = paginator.get_page(page_number)
    
    return render(request, 'productos/mod_productos.html', {
        'productos': productos_paginados,
        'search_term': search_term,
    })
def ver_producto(request, producto_id):
    producto = get_object_or_404(ProductoInventario, id_producto=producto_id)
    return render(request, 'productos/ver_producto.html', {'producto': producto})



def editar_producto(request, producto_id):
    producto = get_object_or_404(ProductoInventario, id_producto=producto_id)

    if request.method == 'POST':
        form = ProductoInventarioForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('mod_productos_home')
        else:
            # Imprimir errores en la consola para depuración
            print(form.errors)
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = ProductoInventarioForm(instance=producto)

    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(ProductoInventario, id_producto=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado exitosamente.')
    return redirect('mod_productos_home')

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoInventarioCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('mod_productos_home')  # Redirigir al panel de productos después de crear
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = ProductoInventarioCreateForm()
    
    return render(request, 'productos/crear_productos.html', {'form': form})


