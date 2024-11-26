from django.shortcuts import render

# Create your views here.
def menu_principal(request):
    return render(request, 'menu_principal.html')
def iniciar_sesion(request):
    return render(request, 'iniciar_sesion.html')