import csv, io
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
import openpyxl

from config.mixins import AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin
from config.permissions import AdminOVendedor
from .models import Pedido
from .serializers import PedidoSerializer
from .filters import PedidoFilter


class PedidoViewSet(AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin, viewsets.ModelViewSet):
    serializer_class   = PedidoSerializer
    filterset_class    = PedidoFilter
    search_fields      = ['numero_pedido', 'cliente__nombre', 'sucursal__nombre']
    ordering_fields    = ['fecha_pedido', 'total', 'estado']
    ordering           = ['-fecha_pedido']
    permission_classes = [AdminOVendedor]

    def get_queryset(self):
        return Pedido.objects.select_related('cliente', 'sucursal').all()

    @extend_schema(tags=['Pedidos'], summary='Listar pedidos')
    def list(self, request, *args, **kwargs): return super().list(request, *args, **kwargs)
    @extend_schema(tags=['Pedidos'], summary='Crear pedido')
    def create(self, request, *args, **kwargs): return super().create(request, *args, **kwargs)
    @extend_schema(tags=['Pedidos'], summary='Ver pedido')
    def retrieve(self, request, *args, **kwargs): return super().retrieve(request, *args, **kwargs)
    @extend_schema(tags=['Pedidos'], summary='Actualizar pedido')
    def update(self, request, *args, **kwargs): return super().update(request, *args, **kwargs)
    @extend_schema(tags=['Pedidos'], summary='Actualizar parcialmente pedido')
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True; return self.update(request, *args, **kwargs)
    @extend_schema(tags=['Pedidos'], summary='Eliminar pedido (soft delete)')
    def destroy(self, request, *args, **kwargs): return super().destroy(request, *args, **kwargs)

    @extend_schema(tags=['Pedidos'], summary='Exportar pedidos')
    @action(detail=False, methods=['get'], url_path='exportar')
    def exportar(self, request):
        fmt   = request.query_params.get('formato', 'excel').lower()
        qs    = self.filter_queryset(self.get_queryset())
        datos = PedidoSerializer(qs, many=True).data
        campos = ['id', 'numero_pedido', 'fecha_pedido', 'estado', 'total']
        if fmt == 'csv':
            resp = HttpResponse(content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename="pedidos.csv"'
            w = csv.DictWriter(resp, fieldnames=campos)
            w.writeheader()
            for r in datos: w.writerow({c: r.get(c, '') for c in campos})
            return resp
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Pedidos'
        ws.append(campos)
        for r in datos: ws.append([str(r.get(c, '')) for c in campos])
        buf = io.BytesIO(); wb.save(buf); buf.seek(0)
        resp = HttpResponse(buf.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        resp['Content-Disposition'] = 'attachment; filename="pedidos.xlsx"'
        return resp
