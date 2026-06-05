from rest_framework import serializers
from api.productos.serializers import ProductoSerializer
from .models import DetallePedido


class DetallePedidoSerializer(serializers.ModelSerializer):
    # Nested serializer (lectura)
    producto_detalle = ProductoSerializer(source='producto', read_only=True)
    # Campo de escritura
    producto = serializers.PrimaryKeyRelatedField(
        queryset=DetallePedido._meta.get_field('producto').related_model.objects.filter(activo=True)
    )

    class Meta:
        model  = DetallePedido
        fields = [
            'id', 'pedido', 'producto', 'producto_detalle',
            'cantidad', 'precio_unitario', 'descuento', 'subtotal',
            'activo', 'fecha_creacion', 'fecha_modificacion',
        ]
        read_only_fields = ['subtotal', 'fecha_creacion', 'fecha_modificacion']
