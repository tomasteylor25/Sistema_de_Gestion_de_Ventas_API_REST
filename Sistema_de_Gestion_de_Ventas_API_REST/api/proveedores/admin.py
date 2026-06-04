from django.contrib import admin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display  = ['nit', 'nombre', 'contacto', 'ciudad', 'activo']
    list_filter   = ['ciudad', 'activo']
    search_fields = ['nombre', 'nit', 'contacto']
    ordering      = ['nombre']
