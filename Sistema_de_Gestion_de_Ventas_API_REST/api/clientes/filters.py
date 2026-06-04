import django_filters
from .models import Cliente


class ClienteFilter(django_filters.FilterSet):
    nombre           = django_filters.CharFilter(lookup_expr='icontains')
    email            = django_filters.CharFilter(lookup_expr='icontains')
    ciudad           = django_filters.CharFilter(lookup_expr='icontains')
    tipo_documento   = django_filters.ChoiceFilter(choices=Cliente.TIPO_DOCUMENTO)
    activo           = django_filters.BooleanFilter()
    fecha_desde      = django_filters.DateFilter(field_name='fecha_creacion', lookup_expr='gte')
    fecha_hasta      = django_filters.DateFilter(field_name='fecha_creacion', lookup_expr='lte')

    class Meta:
        model  = Cliente
        fields = ['nombre', 'email', 'ciudad', 'tipo_documento', 'activo']
