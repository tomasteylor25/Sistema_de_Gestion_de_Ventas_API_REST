import csv, io
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
import openpyxl

from config.mixins import AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin
from config.permissions import SoloLecturaOAdmin
from .models import Producto
from .serializers import ProductoSerializer
from .filters import ProductoFilter


class ProductoViewSet(AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin, viewsets.ModelViewSet):
    serializer_class   = ProductoSerializer
    filterset_class    = ProductoFilter
    search_fields      = ['nombre', 'codigo', 'descripcion']
    ordering_fields    = ['nombre', 'precio', 'stock', 'fecha_creacion']
    ordering           = ['nombre']
    permission_classes = [SoloLecturaOAdmin]

    def get_queryset(self):
        return Producto.objects.select_related('proveedor').all()

    @extend_schema(tags=['Productos'], summary='Listar productos')
    def list(self, request, *args, **kwargs): return super().list(request, *args, **kwargs)
    @extend_schema(tags=['Productos'], summary='Crear producto')
    def create(self, request, *args, **kwargs): return super().create(request, *args, **kwargs)
    @extend_schema(tags=['Productos'], summary='Ver producto')
    def retrieve(self, request, *args, **kwargs): return super().retrieve(request, *args, **kwargs)
    @extend_schema(tags=['Productos'], summary='Actualizar producto')
    def update(self, request, *args, **kwargs): return super().update(request, *args, **kwargs)
    @extend_schema(tags=['Productos'], summary='Actualizar parcialmente producto')
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True; return self.update(request, *args, **kwargs)
    @extend_schema(tags=['Productos'], summary='Eliminar producto (soft delete)')
    def destroy(self, request, *args, **kwargs): return super().destroy(request, *args, **kwargs)

    @extend_schema(tags=['Productos'], summary='Exportar productos')
    @action(detail=False, methods=['get'], url_path='exportar')
    def exportar(self, request):
        fmt   = request.query_params.get('formato', 'excel').lower()
        qs    = self.filter_queryset(self.get_queryset())
        datos = ProductoSerializer(qs, many=True).data
        campos = ['id', 'codigo', 'nombre', 'precio', 'stock', 'unidad_medida']
        if fmt == 'csv':
            resp = HttpResponse(content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename="productos.csv"'
            w = csv.DictWriter(resp, fieldnames=campos)
            w.writeheader()
            for r in datos: w.writerow({c: r.get(c, '') for c in campos})
            return resp
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Productos'
        ws.append(campos)
        for r in datos: ws.append([str(r.get(c, '')) for c in campos])
        buf = io.BytesIO(); wb.save(buf); buf.seek(0)
        resp = HttpResponse(buf.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        resp['Content-Disposition'] = 'attachment; filename="productos.xlsx"'
        return resp
