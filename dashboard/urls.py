from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name='dashboard/login.html',next_page='dshbindex'), name="login"),
    path("logout/", logout_view, name="logout"),
    path("changepassword/", auth_views.PasswordChangeView.as_view(template_name='dashboard/changePassword.html',success_url='login'), name="changepassword"),
    path("listusers/", UserListView.as_view(), name="listusers"),
    path("adduser/", addUser, name="adduser"),
    path("deluser/<int:pk>", delUser, name="deluser"),
    path('index/', index, name="dshbindex"),
    path("listrifas/", DsbListRifas.as_view(), name="listrifas"),
    path("showaddrifa/", dsbShowFormRifas, name="showaddrifas"),
    path("saverifa/", dsbSaveRifas, name="saverifa"),
    path("allrifas/", dsbRifas, name="allrifas"),
    path("delrifa/<int:pk>", dsbDelRifa, name="delrifa"),
    path("disrifa/<int:pk>", dsbDisRifas, name="disrifa"),
    path("showboletosxpagar/", showBoletosPorPagar, name="showboletosxpagar"),
    # path("showboletosxpagar/boletos/<int:pk>", getBoletos, name="boletos"),
    path("showboletosxpagar/boletos/<int:pk>", NumerosListView.as_view(), name="boletos"),
    path("setconfirmpago/<int:pk>", setBoletoPagado, name="setconfirmpago"),
    path("showboletospagados/", showBoletosPagados, name="showboletospagados"),
    # path("showboletospagados/boletos/<int:pk>", getBoletosPagados, name="boletospagados"),
    path("showboletospagados/boletos/<int:pk>", PagadosListView.as_view(), name="boletospagados"),
    path("aplazarpago/", aplazarPago, name="aplazarpago"),
    path("addbono/", addBono, name="addbono"),
    path("delbono/<int:pk>/<int:id_rifa>", delBono, name="delbono"),
    path("updaterifa/<int:pk>", updateRifa, name="updaterifa"),
    path("saveupdatedrifa/", saveUpdatedRifa, name="saveupdatedrifa"),
    path("listcuentas/", ListCuentasBanco.as_view(), name="listcuentas"),
    path("addcuentabanco/", addCuentaBanco, name="addcuentabanco"),
    path("delcuentabanco/<int:pk>", delCuentaBanco, name="delcuentabanco"),
    path("getcuentabanco/<int:pk>", getCuentaBanco, name="getcuentabanco"),
    path("updcuentabanco/", updCuentaBanco, name="updcuentabanco"),
    path("discardboleto/<int:pk>", discardBoleto, name="discardboleto")
]