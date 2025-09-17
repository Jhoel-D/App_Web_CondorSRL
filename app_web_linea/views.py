from django.shortcuts import render
from django.db.models import Q
from app_gral.models import ProductoInventario, Categoria

def sector_informativo(request):
    # --- Filtro por categoría ---
    categoria_id = request.GET.get('categoria')
    # --- Buscador ---
    query = request.GET.get('q')

    productos = ProductoInventario.objects.filter(is_active=True)
    categorias = Categoria.objects.all()

    if categoria_id:
        productos = productos.filter(id_categoria__id=categoria_id)

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(caracteristicas__icontains=query)
        ).distinct()

    context = {
        "productos": productos,
        "categorias": categorias,
        "categoria_id": categoria_id,
        "query": query,
    }
    return render(request, 'sector_informativo.html', context)
