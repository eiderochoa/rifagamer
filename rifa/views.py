from django.shortcuts import render
from .models import *
from .serializers import NumerosSerializer, RifaSerializer
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render(request, template_name='index.html')

def pagos(request):
    return render(request, template_name='pagos.html')

def detalles(request,pk):
    if pk:
        rifa = Rifa.objects.get(id=pk)
        if rifa:
            print(rifa.producto.imagen)
            return render(request, template_name='detalles.html', context={'rifa':rifa})
        else:
            return render(request, template_name='404.html')
    else:
        return render(request, template_name='404.html')

def getNumeros(request,pk):
    if pk:
        numeros = Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).order_by('numero')
        serialized = NumerosSerializer(numeros, many=True)
        return JsonResponse(data=serialized.data, status=200, safe=False)
    else:
        return JsonResponse(data={'msg':'Error'}, status=404)

