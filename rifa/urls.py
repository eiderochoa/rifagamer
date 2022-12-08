from django.urls import path
from .views import *

urlpatterns = [
    path("index/", index, name="index"),
    path("pagos/", pagos, name="pagos"),
    path("detalles/<int:pk>", detalles, name="detalles"),
    path("getnumeros/<int:pk>", getNumeros, name="getnumeros"),
    path("findnumero/<int:pk>", findNumero, name="findnumero"),
    path("addparticipante/", addParicipante, name="addparticipante"),
    path("selecnumero/", selecNumero, name="selecnumero"),
    path("randomnumeros/<int:pk>/<int:num>",getRandomNumero, name="randomnumeros")
]