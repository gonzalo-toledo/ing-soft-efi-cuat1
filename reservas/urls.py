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
        "reservas/",
        ReservaListView.as_view(),
        name="reserva_list"
    ),
    path(
        "reservas/<int:reserva_id>/", 
        ReservaDetailView.as_view(),
        name="reserva_detail"
    ),
    path(
        "reservas/crear/<int:vuelo_id>/<int:asiento_id>/",
        ReservaCreateView.as_view(),
        name="reserva_create"
    ),
    path(
        "reservas/<int:reserva_id>/cancelar/",
        ReservaCancelView.as_view(),
        name="reserva_cancelar",
    ),
    
    # BOLETOS
    path(
        "boletos/",
        BoletoListView.as_view(), 
        name="boleto_list"
    ),
    path(
        "boletos/<int:boleto_id>/",
        BoletoDetailView.as_view(),
        name="boleto_detail"
    ),
    path(
        "boletos/emitir/",
        BoletoCreateView.as_view(),
        name="boleto_create"
    ),
    path(
        "boletos/<int:boleto_id>/anular/",
        BoletoAnularView.as_view(),
        name="boleto_anular",
    ),
]