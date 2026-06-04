"""Modelo base abstracto con campos de auditoría comunes a todas las tablas"""

from django.db import models
from django.contrib.auth.models import User


class ModeloBase(models.Model):
    """
    Modelo abstracto que incluye los campos obligatorios de la guía:
    - activo
    - fecha_creacion
    - fecha_modificacion
    Además agrega auditoría de usuario (creado_por / modificado_por).
    """
    activo            = models.BooleanField(default=True)
    fecha_creacion    = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por        = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_creados'
    )
    modificado_por    = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_modificados'
    )

    class Meta:
        abstract = True

    @classmethod
    def activos(cls):
        return cls.objects.filter(activo=True)
