from django.shortcuts import render, redirect
from rifa.models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rifa.serializers import RifaSerializer


# Create your views here.
def index(request):
    return render(request, template_name="dashboard/index.html")
# class DsbListRifas()
def dsbListRifas(request):
    rifas = Rifa.objects.all()
    return render(request, template_name="dashboard/dsbListRifas.html", context={'rifas':rifas})
def dsbDelRifa(request, pk):
    rifa = Rifa.objects.get(id=pk)
    rifa.delete()
    return redirect('listrifas')
def dsbDisRifas(riquest, pk):
    rifa = Rifa.objects.get(id=pk)
    rifa.stado = '2'
    rifa.save()
    return redirect('listrifas')

def dsbRifas(request):
    rifas = Rifa.objects.all()
    serialized = RifaSerializer(rifas, many=True)
    return JsonResponse(data=serialized.data, status=200, safe=False)

def dsbShowFormRifas(request):
    return render(request, template_name="dashboard/dsbAddRifa.html")

def dsbSaveRifas(request):
    if request.method == "POST":
        imagen = request.FILES.get('imagen')
        descripccion = request.POST.get('descripccion')
        fecha = request.POST.get('daterange')
        fechaArray = fecha.split()
        if imagen != "" and descripccion != "" and fecha !="":
            producto = Producto(nombre=descripccion, imagen= imagen, activo=True)
            producto.save()
            rifa = Rifa(producto=producto,fecha_inicio=fechaArray[0], fecha_fin=fechaArray[2])
            rifa.save()
            channel_layer = get_channel_layer()            
            for i in range(10000):
                print(str(i).zfill(5))
                numero = Numeros(numero=str(i).zfill(5),rifa=rifa)
                numero.save()
                
                async_to_sync(channel_layer.group_send)(
                    'prgbar',
                    {
                        'type': 'chat_message',
                        'message': 'Generando...',
                        'status': str(i+1),
                        'end': '10000'
                    }
                )               


            return JsonResponse(data={'msg':'Done'}, status=201)
        else:
            return JsonResponse(data={'msg':'Error'}, status=400)