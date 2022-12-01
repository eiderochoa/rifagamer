from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, template_name='index.html')

def pagos(request):
    return render(request, template_name='pagos.html')

def detalles(request):
    return render(request, template_name='detalles.html')