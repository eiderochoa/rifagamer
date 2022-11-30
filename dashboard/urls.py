from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name="dshbindex"),
    path("listrifas/", DsbListRifas.as_view(), name="listrifas"),
    path("showaddrifa/", dsbShowFormRifas, name="showaddrifas"),
    path("saverifa/", dsbSaveRifas, name="saverifa"),
    path("allrifas/", dsbRifas, name="allrifas"),
    path("delrifa/<int:pk>", dsbDelRifa, name="delrifa"),
    path("disrifa/<int:pk>", dsbDisRifas, name="disrifa"),
]