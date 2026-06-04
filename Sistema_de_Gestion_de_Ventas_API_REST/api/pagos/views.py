"""ViewSet de Pagos"""

import csv, io, logging
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
import openpyxl

from config.mixins import AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin
from config.permissions import AdminOVendedor
from .models import Pago
from .serializers import PagoSerializer
from .filters import PagoFilter

logger = logging.getLogger('api')


class PagoViewSet(AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin, viewsets.ModelViewSet):
    serializer_class   = PagoSerializer
    filterset_class    = PagoFilter
    search_fields      = ['numero_pago', 'referencia', 'factura__numero_factura']
    ordering_fields    = ['fecha_pago', 'monto', 'estado']
    ordering           = ['-fecha_pago']
    permission_classes = [AdminOVendedor]

    def get_queryset(self):
        return Pago.objects.select_related(
            'factura', 'factura__pedido', 'factura__pedido__cliente'
        ).all()

    @extend_schema(tags=['Pagos'], summary='Listar pagos')
    def list(self, request, *args, **kwargs): return super().list(request, *args, **kwargs)

    @extend_schema(tags=['Pagos'], summary='Registrar pago')
    def create(self, request, *args, **kwargs): return super().create(request, *args, **kwargs)

    @extend_schema(tags=['Pagos'], summary='Ver pago')
    def retrieve(self, request, *args, **kwargs): return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=['Pagos'], summary='Actualizar pago')
    def update(self, request, *args, **kwargs): return super().update(request, *args, **kwargs)

    @extend_schema(tags=['Pagos'], summary='Actualizar parcialmente pago')
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(tags=['Pagos'], summary='Anular pago (soft delete)')
    def destroy(self, request, *args, **kwargs): return super().destroy(request, *args, **kwargs)

    @extend_schema(
        tags=['Pagos'],
        summary='Exportar pagos a Excel o CSV',
        parameters=[
            OpenApiParameter('formato', description='excel o csv', required=False, type=str)
        ]
    )
    @action(detail=False, methods=['get'], url_path='exportar')
    def exportar(self, request):
        fmt   = request.query_params.get('formato', 'excel').lower()
        qs    = self.filter_queryset(self.get_queryset())
        datos = PagoSerializer(qs, many=True).data
        campos = ['id', 'numero_pago', 'fecha_pago', 'monto',
                  'metodo_display', 'estado_display', 'referencia']

        if fmt == 'csv':
            resp = HttpResponse(content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename="pagos.csv"'
            w = csv.DictWriter(resp, fieldnames=campos)
            w.writeheader()
            for r in datos:
                w.writerow({c: r.get(c, '') for c in campos})
            return resp

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Pagos'
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
        resp['Content-Disposition'] = 'attachment; filename="pagos.xlsx"'
        return resp
