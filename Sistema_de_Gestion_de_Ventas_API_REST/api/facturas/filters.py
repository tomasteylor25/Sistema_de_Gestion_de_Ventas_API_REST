import django_filters
from .models import Factura


class FacturaFilter(django_filters.FilterSet):
    estado        = django_filters.ChoiceFilter(choices=Factura.ESTADO)
    pedido        = django_filters.NumberFilter(field_name='pedido__id')
    cliente       = django_filters.NumberFilter(field_name='pedido__cliente__id')
    fecha_desde   = django_filters.DateFilter(field_name='fecha_emision',    lookup_expr='gte')
    fecha_hasta   = django_filters.DateFilter(field_name='fecha_emision',    lookup_expr='lte')
    vence_desde   = django_filters.DateFilter(field_name='fecha_vencimiento', lookup_expr='gte')
    vence_hasta   = django_filters.DateFilter(field_name='fecha_vencimiento', lookup_expr='lte')
    total_min     = django_filters.NumberFilter(field_name='total', lookup_expr='gte')
    total_max     = django_filters.NumberFilter(field_name='total', lookup_expr='lte')
    activo        = django_filters.BooleanFilter()

    class Meta:
        model  = Factura
        fields = ['estado', 'pedido', 'cliente', 'activo']
