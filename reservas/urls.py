from django.urls import path

from reservas.views import (
    BoletoAnularView,
    BoletoCreateView,
    BoletoDetailView,
    BoletoListView,
    ReservaCancelView,
    ReservaCreateView,
    ReservaDetailView,
    ReservaListView,
)

urlpatterns = [
    # RESERVAS
    path(
        "/",
        ReservaListView.as_view(),
        name="reserva_list"
    ),
    path(
        "/<int:reserva_id>/", 
        ReservaDetailView.as_view(),
        name="reserva_detail"
    ),
    path(
        "/crear/<int:vuelo_id>/<int:asiento_id>/",
        ReservaCreateView.as_view(),
        name="reserva_create"
    ),
    path(
        "/<int:reserva_id>/cancelar/",
        ReservaCancelView.as_view(),
        name="reserva_cancelar",
    ),
    
    # BOLETOS
    path(
        "/",
        BoletoListView.as_view(), 
        name="boleto_list"
    ),
    path(
        "/<int:boleto_id>/",
        BoletoDetailView.as_view(),
        name="boleto_detail"
    ),
    path(
        "/emitir/",
        BoletoCreateView.as_view(),
        name="boleto_create"
    ),
    path(
        "/<int:boleto_id>/anular/",
        BoletoAnularView.as_view(),
        name="boleto_anular",
    ),
]