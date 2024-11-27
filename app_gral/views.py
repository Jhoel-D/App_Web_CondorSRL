from django.shortcuts import render,redirect, get_object_or_404

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm #Añadido
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
from .models import Usuario
from django.db.models import Q #para or en python
from django.core.paginator import Paginator


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
    paginator = Paginator(usuarios, 2)  # Mostrar 8 usuarios por página
    page_number = request.GET.get('page')
    usuarios_page = paginator.get_page(page_number)

    # Renderizar la plantilla con los usuarios paginados
    return render(request, 'usuarios/mod_personal/mod_usuarios_home.html', {
        'usuarios': usuarios_page,
        'search_term': search_term
    })


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