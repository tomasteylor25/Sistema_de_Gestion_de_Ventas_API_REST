from rest_framework import serializers
from api.facturas.serializers import FacturaSerializer
from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    # Nested serializer (lectura)
    factura_detalle = FacturaSerializer(source='factura', read_only=True)
    # Campo de escritura
    factura = serializers.PrimaryKeyRelatedField(
        queryset=Pago._meta.get_field('factura').related_model.objects.filter(activo=True)
    )
    estado_display  = serializers.CharField(source='get_estado_display', read_only=True)
    metodo_display  = serializers.CharField(source='get_metodo_pago_display', read_only=True)

    class Meta:
        model  = Pago
        fields = [
            'id', 'numero_pago', 'fecha_pago', 'monto',
            'metodo_pago', 'metodo_display',
            'estado', 'estado_display',
            'referencia',
            'factura', 'factura_detalle',
            'observaciones',
            'activo', 'fecha_creacion', 'fecha_modificacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
