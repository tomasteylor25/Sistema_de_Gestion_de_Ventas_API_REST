from rest_framework import serializers
from api.proveedores.serializers import ProveedorSerializer
from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    # Nested serializer (lectura) — muestra datos del proveedor
    proveedor_detalle = ProveedorSerializer(source='proveedor', read_only=True)
    # Campo de escritura
    proveedor         = serializers.PrimaryKeyRelatedField(
        queryset=Producto._meta.get_field('proveedor').related_model.objects.filter(activo=True)
    )
    stock_bajo        = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Producto
        fields = [
            'id', 'codigo', 'nombre', 'descripcion', 'precio',
            'stock', 'stock_minimo', 'stock_bajo', 'unidad_medida',
            'proveedor', 'proveedor_detalle',
            'activo', 'fecha_creacion', 'fecha_modificacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
