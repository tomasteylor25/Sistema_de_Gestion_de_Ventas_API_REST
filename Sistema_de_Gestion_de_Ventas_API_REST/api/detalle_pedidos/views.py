from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from config.mixins import AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin
from config.permissions import AdminOVendedor
from .models import DetallePedido
from .serializers import DetallePedidoSerializer
from .filters import DetallePedidoFilter


class DetallePedidoViewSet(AuditoriaMixin, SoftDeleteMixin, RespuestaEstandarMixin, viewsets.ModelViewSet):
    serializer_class   = DetallePedidoSerializer
    filterset_class    = DetallePedidoFilter
    search_fields      = ['producto__nombre', 'pedido__numero_pedido']
    ordering_fields    = ['fecha_creacion', 'subtotal']
    ordering           = ['-fecha_creacion']
    permission_classes = [AdminOVendedor]

    def get_queryset(self):
        return DetallePedido.objects.select_related('pedido', 'producto').all()

    @extend_schema(tags=['Detalle Pedidos'], summary='Listar detalles de pedido')
    def list(self, request, *args, **kwargs): return super().list(request, *args, **kwargs)
    @extend_schema(tags=['Detalle Pedidos'], summary='Crear detalle de pedido')
    def create(self, request, *args, **kwargs): return super().create(request, *args, **kwargs)
    @extend_schema(tags=['Detalle Pedidos'], summary='Ver detalle de pedido')
    def retrieve(self, request, *args, **kwargs): return super().retrieve(request, *args, **kwargs)
    @extend_schema(tags=['Detalle Pedidos'], summary='Actualizar detalle de pedido')
    def update(self, request, *args, **kwargs): return super().update(request, *args, **kwargs)
    @extend_schema(tags=['Detalle Pedidos'], summary='Actualizar parcialmente detalle')
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True; return self.update(request, *args, **kwargs)
    @extend_schema(tags=['Detalle Pedidos'], summary='Eliminar detalle (soft delete)')
    def destroy(self, request, *args, **kwargs): return super().destroy(request, *args, **kwargs)
