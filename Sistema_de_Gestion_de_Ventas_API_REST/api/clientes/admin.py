from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['numero_documento', 'nombre', 'apellido', 'email', 'ciudad', 'activo']
    list_filter   = ['tipo_documento', 'ciudad', 'activo']
    search_fields = ['nombre', 'apellido', 'numero_documento', 'email']
    ordering      = ['nombre']
