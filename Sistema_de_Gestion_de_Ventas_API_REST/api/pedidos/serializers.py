from rest_framework import serializers
from api.clientes.serializers import ClienteSerializer
from api.sucursales.serializers import SucursalSerializer
from .models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    # Nested serializers (lectura)
    cliente_detalle  = ClienteSerializer(source='cliente', read_only=True)
    sucursal_detalle = SucursalSerializer(source='sucursal', read_only=True)
    # Campos de escritura
    cliente  = serializers.PrimaryKeyRelatedField(
        queryset=Pedido._meta.get_field('cliente').related_model.objects.filter(activo=True)
    )
    sucursal = serializers.PrimaryKeyRelatedField(
        queryset=Pedido._meta.get_field('sucursal').related_model.objects.filter(activo=True)
    )

    class Meta:
        model  = Pedido
        fields = [
            'id', 'numero_pedido', 'fecha_pedido', 'fecha_entrega', 'estado',
            'cliente', 'cliente_detalle',
            'sucursal', 'sucursal_detalle',
            'observaciones', 'total',
            'activo', 'fecha_creacion', 'fecha_modificacion',
        ]
        read_only_fields = ['total', 'fecha_creacion', 'fecha_modificacion']
