from rest_framework import serializers
from .models import Proveedor


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Proveedor
        fields = ['id', 'nit', 'nombre', 'contacto', 'email', 'telefono',
                  'direccion', 'ciudad', 'sitio_web', 'activo',
                  'fecha_creacion', 'fecha_modificacion']
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
