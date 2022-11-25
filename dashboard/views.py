from django.shortcuts import render, redirect
from rifa.models import *
from .task import generateNumbers

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
            # Create Task
            generateNumber_Task = generateNumbers.delay(rifa.id)
            # Get de Task ID
            task_id = generateNumber_Task.task_id
            # Print Task ID
            print(f'Celery Task ID: {task_id}')
            return render(request, template_name="dashboard/progress.html", context={'task_id': task_id})
        else:
            print("paso algo")