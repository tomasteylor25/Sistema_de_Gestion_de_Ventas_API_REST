from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ['codigo', 'nombre', 'precio', 'stock', 'stock_minimo', 'proveedor', 'activo']
    list_filter   = ['unidad_medida', 'proveedor', 'activo']
    search_fields = ['nombre', 'codigo', 'descripcion']
    ordering      = ['nombre']
    raw_id_fields = ['proveedor']
