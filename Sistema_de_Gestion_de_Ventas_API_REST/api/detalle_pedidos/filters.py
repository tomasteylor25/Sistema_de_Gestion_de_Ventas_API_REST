import django_filters
from .models import DetallePedido


class DetallePedidoFilter(django_filters.FilterSet):
    pedido   = django_filters.NumberFilter(field_name='pedido__id')
    producto = django_filters.NumberFilter(field_name='producto__id')
    activo   = django_filters.BooleanFilter()

    class Meta:
        model  = DetallePedido
        fields = ['pedido', 'producto', 'activo']
