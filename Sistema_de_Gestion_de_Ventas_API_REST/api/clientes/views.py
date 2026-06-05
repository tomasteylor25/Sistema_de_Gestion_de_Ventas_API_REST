"""ViewSet de Clientes con todos los ajustes obligatorios"""

import csv
import logging
import io
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
import openpyxl

from config.mixins import AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin
from config.responses import respuesta_exitosa, respuesta_error
from config.permissions import AdminOVendedor, SoloLecturaOAdmin
from .models import Cliente
from .serializers import ClienteSerializer
from .filters import ClienteFilter

logger = logging.getLogger('api')


class ClienteViewSet(AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin, viewsets.ModelViewSet):
    serializer_class   = ClienteSerializer
    filterset_class    = ClienteFilter
    search_fields      = ['nombre', 'apellido', 'email', 'numero_documento']
    ordering_fields    = ['nombre', 'fecha_creacion', 'ciudad']
    ordering           = ['nombre']
    permission_classes = [AdminOVendedor]

    def get_queryset(self):
        return Cliente.objects.all()

    @extend_schema(tags=['Clientes'], summary='Listar clientes')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=['Clientes'], summary='Crear cliente')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(tags=['Clientes'], summary='Ver cliente')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=['Clientes'], summary='Actualizar cliente')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(tags=['Clientes'], summary='Actualizar parcialmente cliente')
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(tags=['Clientes'], summary='Eliminar cliente (soft delete)')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ── Exportación ──────────────────────────────────────────────────────────
    @extend_schema(
        tags=['Clientes'],
        summary='Exportar clientes a Excel o CSV',
        parameters=[
            OpenApiParameter('formato', description='excel o csv', required=False, type=str)
        ]
    )
    @action(detail=False, methods=['get'], url_path='exportar')
    def exportar(self, request):
        formato   = request.query_params.get('formato', 'excel').lower()
        queryset  = self.filter_queryset(self.get_queryset())
        serializer = ClienteSerializer(queryset, many=True)
        datos      = serializer.data

        campos = ['id', 'tipo_documento', 'numero_documento', 'nombre',
                  'apellido', 'email', 'telefono', 'ciudad', 'activo']

        if formato == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="clientes.csv"'
            writer = csv.DictWriter(response, fieldnames=campos)
            writer.writeheader()
            for row in datos:
                writer.writerow({c: row.get(c, '') for c in campos})
            return response

        # Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Clientes'
        ws.append(campos)
        for row in datos:
            ws.append([str(row.get(c, '')) for c in campos])
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        response = HttpResponse(
            buf.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="clientes.xlsx"'
        return response
