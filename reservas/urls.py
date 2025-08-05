from django.urls import path

from reservas.views import (
    BoletoDetailView,
    BoletoListView,
    BoletoPDFView,
    ReservaCancelView,
    ReservaCreateView,
    ReservaDetailView,
    ReservaListView,
    ReservaConfirmarPagoView,
)

urlpatterns = [
    # RESERVAS
    path(
        "",
        ReservaListView.as_view(),
        name="reserva_list"
    ),
    path(
        "<int:reserva_id>/", 
        ReservaDetailView.as_view(),
        name="reserva_detail"
    ),
    path(
        "crear/<int:vuelo_id>/<int:asiento_id>/",
        ReservaCreateView.as_view(),
        name="reserva_create"
    ),
    path(
        "<int:reserva_id>/confirmar_pago/",
        ReservaConfirmarPagoView.as_view(),
        name="reserva_confirmar_pago"
    ),
    path(
        "<int:reserva_id>/cancelar/",
        ReservaCancelView.as_view(),
        name="reserva_cancelar",
    ),
    
    # BOLETOS
    path(
        "boleto_list/",
        BoletoListView.as_view(), 
        name="boleto_list"
    ),
    path(
        "boleto_detail/<int:boleto_id>/",
        BoletoDetailView.as_view(),
        name="boleto_detail"
    ),
    path(
        "boletos/<int:boleto_id>/descargar-pdf/",
        BoletoPDFView.as_view(),
        name="boleto_pdf"
    ),
    
]