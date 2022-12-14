from django.shortcuts import render
from .models import *
from .serializers import NumerosSerializer, RifaSerializer
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import random
from django.views.defaults import page_not_found
# Create your views here.

def index(request):
    rifas = Rifa.objects.filter(stado='1')
    return render(request, template_name='index.html', context={'rifas':rifas})

def pagos(request):
    return render(request, template_name='pagos.html')

def detalles(request,pk):
    if pk:
        try:
            rifa = Rifa.objects.get(id=pk)
            estados = MXEstados.objects.all()
            if rifa:
                return render(request, template_name='detalles.html', context={'rifa':rifa, 'estados':estados})
            else:
                return render(request, template_name='rifanotfound.html')
        except ObjectDoesNotExist:
            return render(request, template_name='rifanotfound.html')
    else:
        return render(request, template_name='rifanotfound.html')

def getNumeros(request,pk):
    if pk:
        numeros = Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).order_by('numero')
        serialized = NumerosSerializer(numeros, many=True)
        return JsonResponse(data=serialized.data, status=200, safe=False)
    else:
        return JsonResponse(data={'msg':'Error'}, status=404)

def findNumero(request,pk):
    if pk:
        numeros = Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).filter(Q(numero__icontains=request.GET.get('buscar'))).order_by('numero')
        serialized = NumerosSerializer(numeros, many=True)
        return JsonResponse(data=serialized.data, status=200, safe=False)
    else:
        return JsonResponse(data={'msg':'Error'}, status=404)

def addParicipante(request):
    if request.method == "POST":
        if request.POST.get('nombre') != "" and request.POST.get('telefono') !="" and request.POST.get('apellidos') !="":
            participante = Participante(telefono=request.POST.get('telefono'),
            nombre=request.POST.get('nombre'),
            apellidos=request.POST.get('apellidos'),
            mx_stado=MXEstados.objects.get(id=request.POST.get('mx_stado')))
            participante.save()
        return JsonResponse(data={'msg':'OK', 'participante_id':participante.id})
    else:
        return JsonResponse(data={'msg':'Error'})
@csrf_exempt
def selecNumero(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)
        if body['participante_id'] != "" and body['numero'] != "":
            try:
                numero = Numeros.objects.get(id=body['numero'])
                numero.presona = Participante.objects.get(id=body['participante_id'])
                numero.seleccionado = True
                numero.fecha_seleccionado = datetime.now()
                numero.save()
                return JsonResponse(data={'msg':'Boleto actualizado'}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse(data={'msg':'El Boleto no existe'}, status=404)
        else:
            return JsonResponse(data={'msg':'Faltan datos'}, status=404)
    else:
        return JsonResponse(data={'msg':'Metodo no permitido'}, status=404)

def getRandomNumero(request,pk,num):
    if pk and num:
        items = list(Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).filter(seleccionado=False))
        numeros = random.sample(items, num)
        serialized = NumerosSerializer(numeros, many=True)
        return JsonResponse(data=serialized.data, safe=False)
    else:
        return JsonResponse(data={'msg':'Faltan datos'}, status=404)

def error_404_view(request, exception):
    return page_not_found(request,exception=exception, template_name='404.html')
