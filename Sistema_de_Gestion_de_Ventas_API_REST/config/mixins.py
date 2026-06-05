"""Mixins reutilizables para ViewSets"""

import logging
from config.responses import (
    respuesta_exitosa, respuesta_creada,
    respuesta_error, respuesta_no_encontrado, respuesta_eliminado
)

logger = logging.getLogger('api')


class AuditoriaMixin:
    """
    Guarda automáticamente el usuario que crea o modifica un registro
    en los campos creado_por / modificado_por (si existen en el modelo).
    """

    def perform_create(self, serializer):
        kwargs = {}
        modelo = serializer.Meta.model
        if hasattr(modelo, 'creado_por'):
            kwargs['creado_por'] = self.request.user
        if hasattr(modelo, 'modificado_por'):
            kwargs['modificado_por'] = self.request.user
        instance = serializer.save(**kwargs)
        logger.info(
            f'CREAR | {modelo.__name__} id={instance.pk} | '
            f'usuario={self.request.user.username}'
        )

    def perform_update(self, serializer):
        kwargs = {}
        modelo = serializer.Meta.model
        if hasattr(modelo, 'modificado_por'):
            kwargs['modificado_por'] = self.request.user
        instance = serializer.save(**kwargs)
        logger.info(
            f'ACTUALIZAR | {modelo.__name__} id={instance.pk} | '
            f'usuario={self.request.user.username}'
        )


class SoftDeleteMixin:
    """
    Sobreescribe destroy() para hacer eliminación lógica (activo=False).
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not hasattr(instance, 'activo'):
            return respuesta_error('Este modelo no soporta eliminación lógica.')
        instance.activo = False
        instance.save(update_fields=['activo'])
        logger.info(
            f'SOFT-DELETE | {instance.__class__.__name__} id={instance.pk} | '
            f'usuario={request.user.username}'
        )
        return respuesta_eliminado()


class RespuestaEstandarMixin:
    """Devuelve respuestas JSON estandarizadas en create/update/retrieve/list."""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return respuesta_creada(serializer.data)
        return respuesta_error(errores=serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return respuesta_exitosa(serializer.data, 'Registro actualizado correctamente')
        return respuesta_error(errores=serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return respuesta_exitosa(serializer.data)
