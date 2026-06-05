import django_filters
from .models import Pedido


class PedidoFilter(django_filters.FilterSet):
    cliente      = django_filters.NumberFilter(field_name='cliente__id')
    sucursal     = django_filters.NumberFilter(field_name='sucursal__id')
    estado       = django_filters.ChoiceFilter(choices=Pedido.ESTADO)
    fecha_desde  = django_filters.DateFilter(field_name='fecha_pedido', lookup_expr='gte')
    fecha_hasta  = django_filters.DateFilter(field_name='fecha_pedido', lookup_expr='lte')
    total_min    = django_filters.NumberFilter(field_name='total', lookup_expr='gte')
    total_max    = django_filters.NumberFilter(field_name='total', lookup_expr='lte')
    activo       = django_filters.BooleanFilter()

    class Meta:
        model  = Pedido
        fields = ['cliente', 'sucursal', 'estado', 'activo']
