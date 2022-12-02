from django.urls import path
from .views import *

urlpatterns = [
    path("index/", index, name="index"),
    path("pagos/", pagos, name="pagos"),
    path("detalles/<int:pk>", detalles, name="detalles"),
    path("getnumeros/<int:pk>", getNumeros, name="getnumeros")
]