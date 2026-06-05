from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model  = Cliente
        fields = [
            'id', 'tipo_documento', 'numero_documento', 'nombre', 'apellido',
            'nombre_completo', 'email', 'telefono', 'direccion', 'ciudad',
            'activo', 'fecha_creacion', 'fecha_modificacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']

    def get_nombre_completo(self, obj):
        return f'{obj.nombre} {obj.apellido}'.strip()
