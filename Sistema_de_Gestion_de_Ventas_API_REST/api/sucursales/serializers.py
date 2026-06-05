from rest_framework import serializers
from .models import Sucursal


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Sucursal
        fields = ['id', 'codigo', 'nombre', 'direccion', 'ciudad',
                  'telefono', 'email', 'es_principal', 'activo',
                  'fecha_creacion', 'fecha_modificacion']
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
