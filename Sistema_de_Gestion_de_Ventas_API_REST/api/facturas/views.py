"""ViewSet de Facturas"""

import csv, io, logging
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
import openpyxl

from config.mixins import AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin
from config.permissions import AdminOVendedor
from .models import Factura
from .serializers import FacturaSerializer
from .filters import FacturaFilter

logger = logging.getLogger('api')


class FacturaViewSet(AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin, viewsets.ModelViewSet):
    serializer_class   = FacturaSerializer
    filterset_class    = FacturaFilter
    search_fields      = ['numero_factura', 'pedido__numero_pedido', 'pedido__cliente__nombre']
    ordering_fields    = ['fecha_emision', 'fecha_vencimiento', 'total', 'estado']
    ordering           = ['-fecha_emision']
    permission_classes = [AdminOVendedor]

    def get_queryset(self):
        return Factura.objects.select_related(
            'pedido', 'pedido__cliente', 'pedido__sucursal'
        ).all()

    @extend_schema(tags=['Facturas'], summary='Listar facturas')
    def list(self, request, *args, **kwargs): return super().list(request, *args, **kwargs)

    @extend_schema(tags=['Facturas'], summary='Crear factura')
    def create(self, request, *args, **kwargs): return super().create(request, *args, **kwargs)

    @extend_schema(tags=['Facturas'], summary='Ver factura')
    def retrieve(self, request, *args, **kwargs): return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=['Facturas'], summary='Actualizar factura')
    def update(self, request, *args, **kwargs): return super().update(request, *args, **kwargs)

    @extend_schema(tags=['Facturas'], summary='Actualizar parcialmente factura')
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(tags=['Facturas'], summary='Anular factura (soft delete)')
    def destroy(self, request, *args, **kwargs): return super().destroy(request, *args, **kwargs)

    @extend_schema(
        tags=['Facturas'],
        summary='Exportar facturas a Excel o CSV',
        parameters=[
            OpenApiParameter('formato', description='excel o csv', required=False, type=str)
        ]
    )
    @action(detail=False, methods=['get'], url_path='exportar')
    def exportar(self, request):
        fmt   = request.query_params.get('formato', 'excel').lower()
        qs    = self.filter_queryset(self.get_queryset())
        datos = FacturaSerializer(qs, many=True).data
        campos = ['id', 'numero_factura', 'fecha_emision', 'fecha_vencimiento',
                  'estado', 'subtotal', 'iva', 'total', 'cliente_nombre']

        if fmt == 'csv':
            resp = HttpResponse(content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename="facturas.csv"'
            w = csv.DictWriter(resp, fieldnames=campos)
            w.writeheader()
            for r in datos:
                w.writerow({c: r.get(c, '') for c in campos})
            return resp

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Facturas'
        ws.append(campos)
        for r in datos:
            ws.append([str(r.get(c, '')) for c in campos])
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        resp = HttpResponse(
            buf.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        resp['Content-Disposition'] = 'attachment; filename="facturas.xlsx"'
        return resp
