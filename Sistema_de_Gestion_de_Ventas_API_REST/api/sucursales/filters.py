import django_filters
from .models import Sucursal


class SucursalFilter(django_filters.FilterSet):
    nombre       = django_filters.CharFilter(lookup_expr='icontains')
    ciudad       = django_filters.CharFilter(lookup_expr='icontains')
    es_principal = django_filters.BooleanFilter()
    activo       = django_filters.BooleanFilter()

    class Meta:
        model  = Sucursal
        fields = ['nombre', 'ciudad', 'es_principal', 'activo']
