import csv, io
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
import openpyxl

from config.mixins import AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin
from config.permissions import SoloLecturaOAdmin
from .models import Proveedor
from .serializers import ProveedorSerializer
from .filters import ProveedorFilter


class ProveedorViewSet(AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin, viewsets.ModelViewSet):
    serializer_class   = ProveedorSerializer
    filterset_class    = ProveedorFilter
    search_fields      = ['nombre', 'nit', 'ciudad']
    ordering_fields    = ['nombre', 'fecha_creacion']
    ordering           = ['nombre']
    permission_classes = [SoloLecturaOAdmin]

    def get_queryset(self):
        return Proveedor.objects.all()

    @extend_schema(tags=['Proveedores'], summary='Listar proveedores')
    def list(self, request, *args, **kwargs): return super().list(request, *args, **kwargs)
    @extend_schema(tags=['Proveedores'], summary='Crear proveedor')
    def create(self, request, *args, **kwargs): return super().create(request, *args, **kwargs)
    @extend_schema(tags=['Proveedores'], summary='Ver proveedor')
    def retrieve(self, request, *args, **kwargs): return super().retrieve(request, *args, **kwargs)
    @extend_schema(tags=['Proveedores'], summary='Actualizar proveedor')
    def update(self, request, *args, **kwargs): return super().update(request, *args, **kwargs)
    @extend_schema(tags=['Proveedores'], summary='Actualizar parcialmente proveedor')
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True; return self.update(request, *args, **kwargs)
    @extend_schema(tags=['Proveedores'], summary='Eliminar proveedor (soft delete)')
    def destroy(self, request, *args, **kwargs): return super().destroy(request, *args, **kwargs)

    @extend_schema(tags=['Proveedores'], summary='Exportar proveedores')
    @action(detail=False, methods=['get'], url_path='exportar')
    def exportar(self, request):
        fmt    = request.query_params.get('formato', 'excel').lower()
        qs     = self.filter_queryset(self.get_queryset())
        datos  = ProveedorSerializer(qs, many=True).data
        campos = ['id', 'nit', 'nombre', 'contacto', 'email', 'telefono', 'ciudad']
        if fmt == 'csv':
            resp = HttpResponse(content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename="proveedores.csv"'
            w = csv.DictWriter(resp, fieldnames=campos)
            w.writeheader()
            for r in datos: w.writerow({c: r.get(c, '') for c in campos})
            return resp
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Proveedores'
        ws.append(campos)
        for r in datos: ws.append([str(r.get(c, '')) for c in campos])
        buf = io.BytesIO(); wb.save(buf); buf.seek(0)
        resp = HttpResponse(buf.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        resp['Content-Disposition'] = 'attachment; filename="proveedores.xlsx"'
        return resp
