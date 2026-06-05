import django_filters
from .models import Pago


class PagoFilter(django_filters.FilterSet):
    factura      = django_filters.NumberFilter(field_name='factura__id')
    estado       = django_filters.ChoiceFilter(choices=Pago.ESTADO)
    metodo_pago  = django_filters.ChoiceFilter(choices=Pago.METODO)
    fecha_desde  = django_filters.DateFilter(field_name='fecha_pago', lookup_expr='gte')
    fecha_hasta  = django_filters.DateFilter(field_name='fecha_pago', lookup_expr='lte')
    monto_min    = django_filters.NumberFilter(field_name='monto', lookup_expr='gte')
    monto_max    = django_filters.NumberFilter(field_name='monto', lookup_expr='lte')
    activo       = django_filters.BooleanFilter()

    class Meta:
        model  = Pago
        fields = ['factura', 'estado', 'metodo_pago', 'activo']
