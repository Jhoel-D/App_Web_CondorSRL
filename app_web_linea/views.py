from django.shortcuts import render

# Create your views here.
def sector_informativo(request):
    return render(request, 'sector_informativo.html')