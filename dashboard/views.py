from django.shortcuts import render, redirect
from rifa.models import *

# Create your views here.
def index(request):
    return render(request, template_name="dashboard/index.html")

def dsbListRifas(request):
    return render(request, template_name="dashboard/dsbListRifas.html")

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
            for i in range(10000):
                print(str(i).zfill(5))
                numero = Numeros(numero=str(i).zfill(5),rifa=rifa)
                numero.save()
            return redirect('listrifas')
        else:
            print("paso algo")