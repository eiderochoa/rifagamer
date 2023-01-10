from django.shortcuts import render, redirect
from rifa.models import *
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rifa.serializers import RifaSerializer, BonoSerializer
from django.views.generic import ListView, UpdateView
from itertools import islice
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, template_name="dashboard/login.html")
    elif request.method == "POST":
        user = authenticate(username=request.POST.get('username'),password=request.POST.get('password'))
        if user is not None:
            return redirect('dshbindex')
        else:
            return redirect('login')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
    

@permission_required('rifa.view_rifa', 'rifa.view_numeros', raise_exception=True)
def index(request):
    cant_rifas = Rifa.objects.filter(stado='1').count()
    cant_boletos_pagados = Numeros.objects.filter(pagado=True).count()
    cant_boletos_disponibles = Numeros.objects.filter(seleccionado=False).count()
    cant_boletos_x_pagar = Numeros.objects.filter(Q(seleccionado=True) & Q(pagado=False)).count()

    context = {
        'cant_rifas':cant_rifas, 
        'cant_boletos_pagados':cant_boletos_pagados,
        'cant_boletos_disponibles':cant_boletos_disponibles,
        'cant_boletos_x_pagar': cant_boletos_x_pagar
        }
    return render(request, template_name="dashboard/index.html", context=context)

class DsbListRifas(PermissionRequiredMixin,ListView):
    model = Rifa
    template_name = 'dashboard/dsbListRifas.html'
    paginate_by = 10
    permission_required ='rifa.view_rifa'

    def get_context_data(self, **kwargs):
        context = super(DsbListRifas, self).get_context_data(**kwargs)
        if self.request.GET.get('buscar'):
            indice = self.request.GET.get('buscar')
            context['busqueda'] = indice
        return context

    def get_queryset(self):
        queryset = Rifa .objects.all().order_by('-id')         
        return queryset

# @login_required
# @permission_required('rifa.view_rifa')    
# def dsbListRifas(request):
#     rifas = Rifa.objects.all()
#     rifos = Rifa.objects.filter(id=0)
#     return render(request, template_name="dashboard/dsbListRifas.html", context={'rifas':rifos})

@login_required
@permission_required('rifa.delete_rifa')
def dsbDelRifa(request, pk):
    rifa = Rifa.objects.get(id=pk)
    rifa.delete()
    return redirect('listrifas')

@login_required
@permission_required('rifa.change_rifa')
def dsbDisRifas(riquest, pk):
    rifa = Rifa.objects.get(id=pk)
    if rifa.stado == '1':
        rifa.stado = '2'
    elif rifa.stado == '2':
        rifa.stado = '1'
    rifa.save()
    return redirect('listrifas')

@login_required
@permission_required('rifa.view_rifa')
def dsbRifas(request):
    rifas = Rifa.objects.all()
    serialized = RifaSerializer(rifas, many=True)
    return JsonResponse(data=serialized.data, status=200, safe=False)

@login_required
@permission_required('rifa.add_rifa')
def dsbShowFormRifas(request):
    return render(request, template_name="dashboard/dsbAddRifa.html")

@login_required
@permission_required('rifa.can_add_rifa', 'producto.can_add_producto', 'numeros.can_add_numeros')
def dsbSaveRifas(request):
    if request.method == "POST":
        imagen = request.FILES.get('imagen')
        descripccion = request.POST.get('descripccion')
        fecha = request.POST.get('daterange')
        num_posibilidades = request.POST.get('num_posibilidades')
        num_boletos = request.POST.get('num_boletos')
        precio_boleto = request.POST.get('precio_boleto')
        fechaArray = fecha.split()
        if imagen != "" and descripccion != "" and fecha !="" and num_posibilidades != "" and num_boletos != "" and precio_boleto != "":
            producto = Producto(nombre=descripccion, imagen= imagen, activo=True)
            producto.save()
            rifa = Rifa(producto=producto,fecha_inicio=fechaArray[0], fecha_fin=fechaArray[2],num_posibilidades=num_posibilidades, num_boletos=num_boletos, precio_boleto=precio_boleto)
            rifa.save()
            # channel_layer = get_channel_layer()  
            batch_size = 1000      
            objs = (Numeros(numero=str(i).zfill(5),rifa=rifa) for i in range(int(num_boletos)))
            cont = 0
            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                Numeros.objects.bulk_create(batch, batch_size)
                # async_to_sync(channel_layer.group_send)(
                #     'prgbar',
                #     {
                #         'type': 'chat_message',
                #         'message': 'Generando...',
                #         'status': str(cont+1000),
                #         'end': '10000'
                #     }
                # )    
            # for i in range(10000):
            #     numero = Numeros(numero=str(i).zfill(5),rifa=rifa)
            #     numero.save()
                
            #     async_to_sync(channel_layer.group_send)(
            #         'prgbar',
            #         {
            #             'type': 'chat_message',
            #             'message': 'Generando...',
            #             'status': str(i+1),
            #             'end': '10000'
            #         }
            #     )               


            return JsonResponse(data={'msg':'Done', 'id_rifa':rifa.id}, status=201)
        else:
            return JsonResponse(data={'msg':'Llene los campos vacios.'}, status=400)

@login_required
@permission_required('rifa.can_view_rifa')
def showBoletosPorPagar(request):
    rifas = Rifa.objects.filter(stado='1')
    return render(request, template_name='dashboard/dsbBoletosXPagar.html', context={'rifas':rifas})
@login_required
@permission_required('rifa.can_view_rifa','numeros.can_view_numeros')
def getBoletos(request, pk):
    if pk:
        try: 
            boletos = Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).filter(Q(seleccionado=True) & Q(pagado=False))
            rifas = Rifa.objects.filter(stado='1')
            paginator = Paginator(boletos, 10) # Muestra 10 contactos por página.

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, template_name='dashboard/dsbBoletos.html', context={'page_obj':page_obj, 'rifas':rifas, 'id_rifa':pk})
        except ObjectDoesNotExist:
            return JsonResponse(data={'msg':'Objeto no encontrado'}, status=404)

class NumerosListView(PermissionRequiredMixin,ListView):
    model = Numeros
    template_name = "dashboard/dsbBoletos.html"
    permission_required = ('rifa.view_numeros','rifa.change_numeros','rifa.view_rifa')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(NumerosListView, self).get_context_data(**kwargs)
        context['id_rifa'] = self.kwargs['pk']
        context['rifas'] = Rifa.objects.filter(stado='1')
        if self.request.GET.get('buscar'):
            indice = self.request.GET.get('buscar')
            context['busqueda'] = indice            
        return context

    def get_queryset(self):
        pk = self.kwargs['pk']
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).filter(Q(seleccionado=True) & Q(pagado=False) & Q(principal=True) & Q(numero__icontains=buscar))
        else:
            queryset = Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).filter(Q(seleccionado=True) & Q(pagado=False) & Q(principal=True))
        return queryset



@login_required
@permission_required('numeros.can_change_numeros')
def setBoletoPagado(request, pk):
    if pk:
        try:
            boleto = Numeros.objects.get(id=pk)
            boleto.pagado = True
            boleto.fecha_pagado = datetime.now()
            boleto.save()
            boletos = Numeros.objects.filter(id_principal=pk)
            if boletos:
                for boleto in boletos.iterator():
                    boleto.pagado = True
                    boleto.fecha_pagado = datetime.now()
                    boleto.save()                    
            return JsonResponse(data={'msg':'OK'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse(data={'msg':'Error al guardar los datos'},status=400)
@login_required
@permission_required('rifa.can_view_rifa')
def showBoletosPagados(request):
    rifas = Rifa.objects.filter(stado='1')
    return render(request, template_name='dashboard/dsbBoletosPagados.html', context={'rifas':rifas})
@login_required
@permission_required('rifa.view_rifa','rifa.view_numeros')
def getBoletosPagados(request, pk):
    if pk:
        try: 
            boletos = Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).filter(pagado=True)
            rifas = Rifa.objects.filter(stado='1')
            paginator = Paginator(boletos, 10) # Muestra 10 contactos por página.

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, template_name='dashboard/dsbBoletosPag.html', context={'page_obj':page_obj, 'rifas':rifas, 'id_rifa':pk})
        except ObjectDoesNotExist:
            return JsonResponse(data={'msg':'Objeto no encontrado'}, status=404)

class PagadosListView(PermissionRequiredMixin,ListView):
    model = Numeros
    template_name = "dashboard/dsbBoletosPag.html"
    permission_required = ('rifa.view_numeros','rifa.change_numeros','rifa.view_rifa')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PagadosListView, self).get_context_data(**kwargs)
        context['id_rifa'] = self.kwargs['pk']
        context['rifas'] = Rifa.objects.filter(stado='1')
        if self.request.GET.get('buscar'):
            indice = self.request.GET.get('buscar')
            context['busqueda'] = indice            
        return context

    def get_queryset(self):
        pk = self.kwargs['pk']
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).filter(Q(pagado=True) & Q(numero__icontains=buscar))
        else:
            queryset = Numeros.objects.filter(rifa=Rifa.objects.get(id=pk)).filter(pagado=True)
        return queryset


class UserListView(ListView):
    model = User
    template_name = "dashboard/listUsers.html"
    paginate_by = 10
    permission_required = 'auth.view_user'

    

@login_required
@permission_required('auth.add_user')
def addUser(request):
    if request.method == 'GET':
        return render(request, template_name="dashboard/addUser.html")
    elif request.method == 'POST':
        user = User.objects.create_user(request.POST.get('username'),request.POST.get('email'),request.POST.get('password1'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        content_type = ContentType.objects.get_for_model(Rifa)
        content_type1 = ContentType.objects.get_for_model(Numeros)
        content_type2 = ContentType.objects.get_for_model(Producto)
        content_type3 = ContentType.objects.get_for_model(Participante())

        user.user_permissions.add(
            Permission.objects.get(codename='view_rifa', content_type=content_type),
            Permission.objects.get(codename='change_rifa', content_type=content_type),
            Permission.objects.get(codename='delete_rifa', content_type=content_type),
            Permission.objects.get(codename='add_rifa', content_type=content_type),
            Permission.objects.get(codename='view_numeros', content_type=content_type1),
            Permission.objects.get(codename='change_numeros', content_type=content_type1),
            Permission.objects.get(codename='delete_numeros', content_type=content_type1),
            Permission.objects.get(codename='add_numeros', content_type=content_type1),
            Permission.objects.get(codename='add_producto', content_type=content_type2),
            Permission.objects.get(codename='add_participante', content_type=content_type3),
            )
        user.save()
        return redirect('listusers')
@login_required
@permission_required('auth.delete_user')
def delUser(request, pk):
    if pk:
        try:
            user = User.objects.get(id=pk)
            user.delete()
            return redirect('listusers')
        except ObjectDoesNotExist:
            return JsonResponse(data={'msg': 'El usuario no existe'}, status=404)

@login_required
@permission_required('rifa.change_numeros')
def aplazarPago(request):
    if request.method == "POST":
        if request.POST.get('horas') and request.POST.get('id_boleto'):
            boleto = Numeros.objects.get(id=request.POST.get('id_boleto'))
            boleto.fecha_seleccionado = boleto.fecha_seleccionado + timedelta(hours=int(request.POST.get('horas')))
            boleto.save()
            return JsonResponse(data={'msg':'OK'},status=200)
        else:
            return JsonResponse(data={'msg':'Error'},status=400)
    else:
        return JsonResponse(data={'msg':'Metodo no perminido'},status=400)

@login_required
@permission_required('rifa.add_bono', 'rifa.view_bono')
def addBono(request):
    if request.method == "POST":
        if request.POST.get('id_rifa'):
            rifa = Rifa.objects.get(id=request.POST.get('id_rifa'))
            bono = Bono(rifa=rifa, condiciones=request.POST.get('condiciones'),premio=request.POST.get('premio'))
            bono.save()
            bonos = Bono.objects.filter(rifa=rifa)
            serialized = BonoSerializer(bonos, many=True)
            return JsonResponse(data=serialized.data, status=201, safe=False)
        else:
            return JsonResponse(data={"msg":"Rifa no encontrada"}, status=400)

    else:
        return JsonResponse(data={"msg":"Metodo no permitido"}, status=400) 

@login_required
@permission_required('rifa.remove_bono')
def delBono(request, pk, id_rifa):
    if pk:
        bono = Bono.objects.get(id=pk)
        bono.delete()
        rifa = Rifa.objects.get(id=id_rifa)
        bonos = Bono.objects.filter(rifa=rifa)
        serialized = BonoSerializer(bonos, many=True)
        return JsonResponse(data=serialized.data, status=201, safe=False)
    else:
        return JsonResponse(data={"msg":"Faltan datos"}, status=400)

@login_required
@permission_required('rifa.view_bono', 'rifa.view_bono')
def updateRifa(request, pk):
    if pk:
        try:
            rifa = Rifa.objects.get(id=pk)
            bonos = Bono.objects.filter(rifa=rifa)
            return render(request, template_name='dashboard/dsbUpdateRifa.html', context={'rifa':rifa, 'bonos':bonos})
        except ObjectDoesNotExist:
            return JsonResponse(data={"msg":"Rifa no encontrada"}, status=404)
    else:
        return JsonResponse(data={"msg":"Faltan datos"}, status=400)

@login_required
@permission_required('rifa.update_producto', 'rifa.update_rifa')
def saveUpdatedRifa(request):
    if request.method == "POST":
        rifa = Rifa.objects.get(id=request.POST.get('id_rifa'))
        producto = rifa.producto        
        imagen = request.FILES.get('imagen')
        descripccion = request.POST.get('descripccion')
        fecha = request.POST.get('daterange')
        num_posibilidades = request.POST.get('num_posibilidades')        
        if descripccion != "" and num_posibilidades != "" :            
            if imagen != None:
                producto.imagen = imagen
            producto.nombre = descripccion
            producto.save()
            if fecha != "":
                fechaArray = fecha.split()
                rifa.fecha_inicio = fechaArray[0]
                rifa.fecha_fin = fechaArray[2]
            rifa.num_posibilidades = num_posibilidades
            rifa.save()
            return JsonResponse(data={'msg':'Datos actualizados Correctamente'}, status=200)
        else:
            return JsonResponse(data={'msg':'Faltan datos'}, status=400)
        

        

