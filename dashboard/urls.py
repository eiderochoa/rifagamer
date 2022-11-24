from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name="dshbindex"),
    path("listrifas/", dsbListRifas, name="listrifas"),
    path("showaddrifa/", dsbShowFormRifas, name="showaddrifas"),
    path("saverifa/", dsbSaveRifas, name="saverifa")
]