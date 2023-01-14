from django.db import models
from django.conf import settings
from PIL import Image
from django_resized import ResizedImageField
# Create your models here.
class MXEstados(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Participante(models.Model):
    telefono = models.CharField(max_length=10)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    mx_stado = models.ForeignKey(MXEstados, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre+' '+self.apellidos+' - '+self.telefono
    

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    imagen = ResizedImageField(size=[950,670], quality=75, upload_to="productosimg/")
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        super(Producto, self).save(*args, **kwargs)
        img = Image.open(self.imagen.path)
        if img.width > 950 or img.height > 670:
            output_size = (950, 670)


class Rifa(models.Model):
    STADO=(
        ('1','Activa'),
        ('2','Cerrada')
    )
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    stado = models.CharField(max_length=1, choices=STADO, default='1')
    num_posibilidades = models.IntegerField(default=1)
    num_boletos = models.IntegerField(default=10000)
    precio_boleto = models.FloatField(default=199)
    

class Numeros(models.Model):
    numero = models.CharField(max_length=5)
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE)
    seleccionado = models.BooleanField(default=False)
    fecha_seleccionado = models.DateTimeField(blank=True, null=True)
    pagado = models.BooleanField(default=False)
    fecha_pagado = models.DateTimeField(blank=True, null=True)
    ganador = models.BooleanField(default=False)
    participante = models.ForeignKey(Participante, on_delete=models.DO_NOTHING, blank=True, null=True)
    principal = models.BooleanField(default=False)
    secundario = models.BooleanField(default=False)
    id_principal = models.IntegerField(default=0, blank=True, null=True)

class Bono(models.Model):
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE, default=1)
    condiciones = models.CharField(max_length=255, default="Condicion")
    premio = models.CharField(max_length=200, default="20,000 MXN")

class CuentaBanco(models.Model):
    TIPO_TRANSACCION = (
        ('1', 'Trasferencia y Cajero'),
        ('2', 'OXXO y Seven')
    )
    num_cuenta = models.CharField(max_length=16)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    banco = models.CharField(max_length=50)
    tipo_transaccion = models.CharField(max_length=1, choices=TIPO_TRANSACCION)





