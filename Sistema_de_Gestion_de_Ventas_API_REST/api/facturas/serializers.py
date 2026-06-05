from rest_framework import serializers
from api.pedidos.serializers import PedidoSerializer
from .models import Factura


class FacturaSerializer(serializers.ModelSerializer):
    # Nested serializer (lectura)
    pedido_detalle = PedidoSerializer(source='pedido', read_only=True)
    # Campo de escritura
    pedido = serializers.PrimaryKeyRelatedField(
        queryset=Factura._meta.get_field('pedido').related_model.objects.filter(activo=True)
    )
    cliente_nombre = serializers.SerializerMethodField()

    class Meta:
        model  = Factura
        fields = [
            'id', 'numero_factura', 'fecha_emision', 'fecha_vencimiento', 'estado',
            'pedido', 'pedido_detalle', 'cliente_nombre',
            'subtotal', 'iva', 'total',
            'observaciones',
            'activo', 'fecha_creacion', 'fecha_modificacion',
        ]
        read_only_fields = ['total', 'fecha_creacion', 'fecha_modificacion']

    def get_cliente_nombre(self, obj):
        c = obj.pedido.cliente
        return f'{c.nombre} {c.apellido}'.strip()
