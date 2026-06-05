from django.contrib import admin
from .models import Sucursal


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display  = ['codigo', 'nombre', 'ciudad', 'es_principal', 'activo']
    list_filter   = ['ciudad', 'es_principal', 'activo']
    search_fields = ['nombre', 'codigo', 'ciudad']
    ordering      = ['nombre']
