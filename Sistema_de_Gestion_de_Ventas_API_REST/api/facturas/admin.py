from django.contrib import admin
from .models import Factura


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display    = ['numero_factura', 'pedido', 'estado', 'subtotal', 'iva', 'total',
                       'fecha_emision', 'fecha_vencimiento', 'activo']
    list_filter     = ['estado', 'activo']
    search_fields   = ['numero_factura', 'pedido__numero_pedido']
    ordering        = ['-fecha_emision']
    raw_id_fields   = ['pedido']
    readonly_fields = ['total']
