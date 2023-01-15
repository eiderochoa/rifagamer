from django.urls import path
from .views import *

urlpatterns = [
    path("index/", index, name="index"),
    path("pagos/", pagos, name="pagos"),
    path("aviso-privacidad/", avisoPrivacidad, name="aviso-privacidad"),
    path("detalles/<int:pk>", detalles, name="detalles"),
    path("getnumeros/<int:pk>", getNumeros, name="getnumeros"),
    path("findnumero/<int:pk>", findNumero, name="findnumero"),
    path("addparticipante/", addParicipante, name="addparticipante"),
    path("selecnumero/", selecNumero, name="selecnumero"),
    path("randomnumeros/<int:pk>/<int:num>",getRandomNumero, name="randomnumeros"),
    path("getposibilidades/<int:pk>", getPosibilidades, name="getposibilidades"),
    path("getboletoid/<int:pk>/<str:boleto>", getBoletoId, name="getboletoid"),
    path("vincularposibilidades/", vincularPosibilidades, name="vincularposibilidades"),
    path("checarboleto/<int:pk>", showChecarBoleto, name="checarboleto"),
    path("chkboleto/", checkarBoleto, name="chkboleto"),
    path("notfound/", notFound, name="notfound")

]