from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from config.mixins import AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin
from config.permissions import SoloLecturaOAdmin
from .models import Sucursal
from .serializers import SucursalSerializer
from .filters import SucursalFilter


class SucursalViewSet(AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin, viewsets.ModelViewSet):
    serializer_class   = SucursalSerializer
    filterset_class    = SucursalFilter
    search_fields      = ['nombre', 'ciudad', 'codigo']
    ordering_fields    = ['nombre', 'ciudad', 'fecha_creacion']
    ordering           = ['nombre']
    permission_classes = [SoloLecturaOAdmin]

    def get_queryset(self):
        return Sucursal.objects.all()

    @extend_schema(tags=['Sucursales'], summary='Listar sucursales')
    def list(self, request, *args, **kwargs): return super().list(request, *args, **kwargs)
    @extend_schema(tags=['Sucursales'], summary='Crear sucursal')
    def create(self, request, *args, **kwargs): return super().create(request, *args, **kwargs)
    @extend_schema(tags=['Sucursales'], summary='Ver sucursal')
    def retrieve(self, request, *args, **kwargs): return super().retrieve(request, *args, **kwargs)
    @extend_schema(tags=['Sucursales'], summary='Actualizar sucursal')
    def update(self, request, *args, **kwargs): return super().update(request, *args, **kwargs)
    @extend_schema(tags=['Sucursales'], summary='Actualizar parcialmente sucursal')
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True; return self.update(request, *args, **kwargs)
    @extend_schema(tags=['Sucursales'], summary='Eliminar sucursal (soft delete)')
    def destroy(self, request, *args, **kwargs): return super().destroy(request, *args, **kwargs)
