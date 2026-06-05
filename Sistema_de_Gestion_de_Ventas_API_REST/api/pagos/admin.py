from django.contrib import admin
from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display  = ['numero_pago', 'factura', 'monto', 'metodo_pago', 'estado',
                     'referencia', 'fecha_pago', 'activo']
    list_filter   = ['estado', 'metodo_pago', 'activo']
    search_fields = ['numero_pago', 'referencia', 'factura__numero_factura']
    ordering      = ['-fecha_pago']
    raw_id_fields = ['factura']
