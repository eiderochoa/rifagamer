from django.db import models

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
    imagen = models.ImageField()
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Rifa(models.model):
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateField()
    

class Numeros(models.Model):
    numero = models.CharField(max_length=5)
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE)
    seleccionado = models.BooleanField(default=False)
    fecha_seleccionado = models.DateTimeField()
    pagado = models.BooleanField(default=False)
    fecha_pagado = models.DateTimeField()
    presona = models.ForeignKey(Participante, on_delete=models.DO_NOTHING)