import django_filters
from .models import Proveedor


class ProveedorFilter(django_filters.FilterSet):
    nombre  = django_filters.CharFilter(lookup_expr='icontains')
    ciudad  = django_filters.CharFilter(lookup_expr='icontains')
    activo  = django_filters.BooleanFilter()

    class Meta:
        model  = Proveedor
        fields = ['nombre', 'ciudad', 'activo']
