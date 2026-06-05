import django_filters
from .models import Producto


class ProductoFilter(django_filters.FilterSet):
    nombre       = django_filters.CharFilter(lookup_expr='icontains')
    proveedor    = django_filters.NumberFilter(field_name='proveedor__id')
    precio_min   = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max   = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    stock_bajo   = django_filters.BooleanFilter(method='filtrar_stock_bajo')
    activo       = django_filters.BooleanFilter()

    def filtrar_stock_bajo(self, queryset, name, value):
        from django.db.models import F
        if value:
            return queryset.filter(stock__lte=F('stock_minimo'))
        return queryset.filter(stock__gt=F('stock_minimo'))

    class Meta:
        model  = Producto
        fields = ['nombre', 'proveedor', 'activo']
