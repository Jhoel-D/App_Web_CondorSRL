from django.shortcuts import render,redirect, get_object_or_404

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm #Añadido
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
from .models import Usuario, ProductoInventario, Categoria, Ventas, ProductosVenta
from django.db.models import Q #para or en python
from django.core.paginator import Paginator

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UsuarioUpdateForm, ProductoInventarioForm, ProductoInventarioCreateForm, UsuarioForm, UsuarioCreateForm, CategoriaForm, CategoriaCreateForm, ProductosVentaForm, VentasForm


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
#MOD USUARIOS
@login_required
def mod_usuarios_home(request):
    # Obtener el grupo "Cliente"
    grupo_clientes = Group.objects.get(name='Cliente')

    # Filtrar usuarios excluyendo los del grupo "Cliente"
    todos_usuarios = Usuario.objects.exclude(groups=grupo_clientes)

    # Separar usuarios activos e inactivos
    usuarios_activos = todos_usuarios.filter(is_active=True)
    usuarios_inactivos = todos_usuarios.filter(is_active=False)

    # Filtro de búsqueda
    search_term = request.GET.get('search', '')
    if search_term:
        usuarios_activos = usuarios_activos.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(CI__icontains=search_term) |
            Q(username__icontains=search_term)
        )
        usuarios_inactivos = usuarios_inactivos.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(CI__icontains=search_term) |
            Q(username__icontains=search_term)
        )

    # Paginación para usuarios activos
    paginator_activos = Paginator(usuarios_activos, 6)  # 10 usuarios activos por página
    page_number_activos = request.GET.get('page_activos')
    usuarios_activos_page = paginator_activos.get_page(page_number_activos)

    # Paginación para usuarios inactivos
    paginator_inactivos = Paginator(usuarios_inactivos, 6)  # 10 usuarios inactivos por página
    page_number_inactivos = request.GET.get('page_inactivos')
    usuarios_inactivos_page = paginator_inactivos.get_page(page_number_inactivos)

    # Renderizar la plantilla con usuarios paginados
    return render(request, 'usuarios/mod_personal/mod_usuarios_home.html', {
        'usuarios_activos': usuarios_activos_page,
        'usuarios_inactivos': usuarios_inactivos_page,
        'search_term': search_term
    })

def ver_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'usuarios/mod_personal/ver_usuario.html', {'usuario': usuario})


# from django.http import Http404

# def ver_usuario(request, usuario_id):
#     try:
#         usuario = Usuario.objects.get(id=usuario_id, is_active=True)
#     except Usuario.DoesNotExist:
#         raise Http404("Usuario no encontrado o inactivo.")
#     return render(request, 'usuarios/mod_personal/ver_usuario.html', {'usuario': usuario})

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

def eliminar_usuario(request, usuario_id):
    # usuario = get_object_or_404(Usuario, id=usuario_id)
    # usuario.delete()
    # messages.success(request, 'Usuario eliminado exitosamente.')
    # return redirect('mod_usuarios_home')
     # Obtener el usuario o retornar 404 si no se encuentra
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Cambiar el estado del usuario
    if usuario.is_active:
        usuario.is_active = False  # Desactivar el usuario (Dado de baja)
        estado = "Dado de baja"
    else:
        usuario.is_active = True   # Activar el usuario
        estado = "Activo"

    usuario.save()  # Guardar los cambios en el estado

    # Mostrar un mensaje de éxito
    messages.success(request, f'Usuario {estado} exitosamente.')

    # Redirigir a la vista de la lista de usuarios
    return redirect('mod_usuarios_home')

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
    usuarios = usuarios.filter(is_active=True)

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
def ver_cliente(request, cliente_id):
    cliente = get_object_or_404(Usuario, id=cliente_id)
    return render(request, 'usuarios/mod_cliente/ver_cliente.html', {'cliente': cliente})


def editar_cliente(request, cliente_id):
    usuario = get_object_or_404(Usuario, id=cliente_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente editado exitosamente.')
            return redirect('mod_clientes_home')
        else:
            # Imprimir errores en la consola para depuración
            print(form.errors)
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/mod_cliente/editar_cliente.html', {'form': form, 'usuario': usuario})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Usuario, id=cliente_id)

    # Cambiar el estado del usuario
    if cliente.is_active:
        cliente.is_active = False  # Desactivar el usuario (Dado de baja)
        estado = "Dado de baja"
    else:
        cliente.is_active = True   # Activar el usuario
        estado = "Activo"

    cliente.save()  # Guardar los cambios en el estado

    # Mostrar un mensaje de éxito
    messages.success(request, f'Cliente {estado} exitosamente.')

    # Redirigir a la vista de la lista de usuarios
    return redirect('mod_clientes_home')

def registrar_cliente(request):
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Esto ya maneja la asociación del grupo en el método save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('mod_clientes_home')  # Redirige al home o la página deseada
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = UsuarioCreateForm()
    
    return render(request, 'usuarios/mod_cliente/registrar_cliente.html', {'form': form})
#MOD ROLES
@login_required
def roles_list(request):
    roles = Group.objects.all().order_by('id')
    return render(request, 'usuarios/mod_personal/roles_list.html', {'roles': roles})


# Agregar Rol
def agregar_rol(request):
    if request.method == 'POST':
        nombre_rol = request.POST.get('nombre')
        if nombre_rol:
            if not Group.objects.filter(name=nombre_rol).exists():
                Group.objects.create(name=nombre_rol)
                messages.success(request, 'Rol creado exitosamente.')
            else:
                messages.error(request, 'Ya existe un rol con ese nombre.')
            return redirect('roles_list')
        else:
            messages.error(request, 'El nombre del rol no puede estar vacío.')
    return render(request, 'usuarios/mod_personal/agregar_rol.html')

# Editar Rol
def editar_rol(request, rol_id):
    rol = get_object_or_404(Group, id=rol_id)
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre')
        if nuevo_nombre:
            if not Group.objects.filter(name=nuevo_nombre).exclude(id=rol_id).exists():
                rol.name = nuevo_nombre
                rol.save()
                messages.success(request, 'Rol actualizado exitosamente.')
            else:
                messages.error(request, 'Ya existe un rol con ese nombre.')
            return redirect('roles_list')
        else:
            messages.error(request, 'El nombre del rol no puede estar vacío.')
    return render(request, 'usuarios/mod_personal/editar_rol.html', {'rol': rol})

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

#MOD CATEGORíAs
def mod_categorias_home(request):
    search_term = request.GET.get('search', '')
    categoria = Categoria.objects.filter(is_active=True)
    categoria = categoria.filter(nombre__icontains=search_term)
    
    categorias_inactivas = Categoria.objects.filter(is_active=False)
    
    
    # Paginación
    paginator = Paginator(categoria, 5)  # Muestra 10 productos por página
    page_number = request.GET.get('page')  # Número de página desde la URL
    categorias_paginadas = paginator.get_page(page_number)
    
    return render(request, 'categorias/mod_categorias.html', {
        'categoria': categorias_paginadas,
        'search_term': search_term,
    })



def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id_categoria=categoria_id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('mod_categorias_home')
        else:
            # Imprimir errores en la consola para depuración
            print(form.errors)
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categorias/editar_categoria.html', {'form': form, 'categoria': categoria})

def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id_categoria=categoria_id)

    # Cambiar el estado del usuario
    if categoria.is_active:
        categoria.is_active = False  # Desactivar el usuario (Dado de baja)
        estado = "Dado de baja"
    else:
        categoria.is_active = True   # Activar el usuario
        estado = "Activo"

    categoria.save()  # Guardar los cambios en el estado

    # Mostrar un mensaje de éxito
    messages.success(request, f'Categoría {estado} exitosamente.')

    # Redirigir a la vista de la lista de usuarios
    return redirect('mod_categorias_home')


def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('mod_categorias_home')  # Redirigir al panel de productos después de crear
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = CategoriaCreateForm()
    
    return render(request, 'categorias/crear_categorias.html', {'form': form})



#MOD VENTAS
@login_required  
def mod_ventas_home(request):
    # Obtener las ventas
    # ventas = Ventas.objects.all()
    ventas = Ventas.objects.filter(is_active=True)
    search_term = request.GET.get('search', '')
    if search_term:
        ventas = ventas.filter(
            
            Q(id_venta__icontains=search_term)
        )

    # Paginación
    paginator = Paginator(ventas, 8)  # Mostrar 8 clientes por página
    page_number = request.GET.get('page')
    ventas_page = paginator.get_page(page_number)

    return render(request, 'ventas/mod_ventas_home.html', {
        'ventas': ventas_page,
        'search_term': search_term
    })

def ver_productos_venta(request, venta_id):
    # Obtener la venta y los productos relacionados
    venta = get_object_or_404(Ventas, id_venta=venta_id)
    productos = ProductosVenta.objects.filter(venta=venta)  # Suponiendo que DetalleVenta enlaza venta y productos
    
    context = {
        'venta': venta,
        'productos': productos,
    }
    return render(request, 'ventas/ver_productos_venta.html', context)



def ver_detalle_venta(request, venta_id):
    # Obtener la venta y los productos asociados
    venta = get_object_or_404(Ventas, id_venta=venta_id)
    productos = ProductosVenta.objects.filter(venta=venta)
    
    context = {
        'venta': venta,
        'productos': productos,
    }
    return render(request, 'ventas/ver_detalle_venta.html', context)


# views.py
from django.forms import modelformset_factory
def editar_venta(request, venta_id):
    # Obtener la venta existente
    venta = get_object_or_404(Ventas, id_venta=venta_id)
    ItemFormSet = modelformset_factory(
        ProductosVenta, form=ProductosVentaForm, extra=1, can_delete=True
    )
    
    if request.method == "POST":
        venta_form = VentasForm(request.POST, instance=venta)
        items_formset = ItemFormSet(
            request.POST,
            queryset=ProductosVenta.objects.filter(venta=venta)
        )
        
        if venta_form.is_valid() and items_formset.is_valid():
            # Primero, manejar eliminaciones
            for form in items_formset.deleted_forms:
                if form.instance.pk:  # Asegurarse de que el objeto exista en la BD
                    form.instance.delete()
                else:
                    form.save(commit=False).delete()

            # Luego, procesar los formularios restantes
            for form in items_formset:
                if form.cleaned_data.get('DELETE', False):  # Omite eliminados
                    continue

                producto_venta = form.save(commit=False)
                producto_venta.venta = venta

                # Validar que el producto exista y esté asociado correctamente
                producto = form.cleaned_data.get('producto')
                if producto:
                    try:
                        producto_venta.producto = ProductoInventario.objects.get(
                            id_producto=producto.id_producto
                        )
                    except ProductoInventario.DoesNotExist:
                        form.add_error('producto', 'El producto relacionado ya no existe.')
                        continue
                else:
                    form.add_error('producto', 'El campo producto es obligatorio.')
                    continue

                # Guardar producto de la venta
                producto_venta.save()

            # Guardar la venta después de procesar los productos
            venta_form.save()

            # Redirigir al editar venta
            return redirect('editar_venta', venta_id=venta.id_venta)
            
    else:
        # Si es un GET, inicializa los formularios
        venta_form = VentasForm(instance=venta)
        items_formset = ItemFormSet(
            queryset=ProductosVenta.objects.filter(venta=venta)
        )

    # Renderizar el template con los formularios
    return render(request, 'ventas/editar_venta.html', {
        'venta_form': venta_form,
        'items_formset': items_formset,
        'costo_total': venta.calcular_costo_total()
    })

def dar_de_baja_venta(request, venta_id):
    venta = get_object_or_404(Ventas, id_venta=venta_id)
    if venta.is_active == True:
        venta.is_active = False
        estado = "Dado de baja"
    else:
        venta.is_active = True
        estado = "Activo"
    venta.save()
    messages.success(request, f'Venta {estado} exitosamente.')
    return redirect('mod_ventas_home')

@login_required
#  ventas = Ventas.objects.filter(is_active=True)
def imprimir_venta(request, venta_id):
    ventas = get_object_or_404(Ventas, id_venta=venta_id)
    productos = ProductosVenta.objects.filter(venta=ventas) # Obtener los productos de la venta

    return render(request, 'ventas/imprimir_venta.html', {
        'ventas': ventas,
        'productos': productos,
    })

def add_sale(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)

        if venta_form.is_valid():
            venta = venta_form.save(commit=False)
            venta.save()
            
            # Procesar los productos enviados desde el formulario
            productos_data = request.POST.getlist('productos[]')
            cantidades_data = request.POST.getlist('cantidades[]')
            precios_data = request.POST.getlist('precios[]')
            
            for nombre, cantidad, precio in zip(productos_data, cantidades_data, precios_data):
                if nombre and cantidad and precio:
                    producto = ProductoInventario(
                        venta=venta,
                        nombre=nombre,
                        cantidad=int(cantidad),
                        precio_unitario=float(precio)
                    )
                    producto.save()
            
            return redirect('some_success_url')
    else:
        venta_form = VentasForm()

    return render(request, 'ventas/add_sale.html', {'venta_form': venta_form})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction
from .models import Ventas, ProductosVenta, ProductoInventario
from .forms import VentasForm

@login_required
@transaction.atomic
def crear_venta(request):
    if request.method == 'POST':
        venta_form = VentasForm(request.POST)
        if venta_form.is_valid():
            # Crear la venta, asignando el vendedor al usuario logueado
            venta = venta_form.save(commit=False)
            venta.id_vendedor = request.user  # Asigna el usuario logueado como vendedor
            venta.save()

            # Procesar los productos relacionados
            productos_data = request.POST.getlist('productos[]')
            for producto_data in productos_data:
                producto_id = producto_data.get('producto_id')
                cantidad = int(producto_data.get('cantidad'))
                try:
                    producto = ProductoInventario.objects.get(pk=producto_id)
                    ProductosVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad,
                    )
                except ProductoInventario.DoesNotExist:
                    return JsonResponse({'error': f"Producto con ID {producto_id} no existe"}, status=400)

            return redirect('mod_ventas_home')
            # return JsonResponse({'success': True, 'redirect_url': '/ventas/'})
        else:
            return JsonResponse({'success': False, 'errors': venta_form.errors}, status=400)
    else:
        venta_form = VentasForm()
        return render(request, 'ventas/crear_venta.html', {'form': venta_form})
