from django.urls import path
from .views import *

urlpatterns = [
    path("index/", index, name="index"),
    path("pagos/", pagos, name="pagos"),
    path("detalles/", detalles, name="detalles")
]