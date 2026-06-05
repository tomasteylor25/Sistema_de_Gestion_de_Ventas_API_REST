"""Manejador de excepciones personalizado"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        mensaje_mapa = {
            400: 'Solicitud incorrecta',
            401: 'No autenticado. Por favor inicia sesión.',
            403: 'No tienes permisos para realizar esta acción.',
            404: 'El recurso solicitado no fue encontrado.',
            405: 'Método no permitido.',
            500: 'Error interno del servidor.',
        }
        codigo = response.status_code
        return Response({
            'success': False,
            'message': mensaje_mapa.get(codigo, 'Error en la operación'),
            'errors':  response.data,
        }, status=codigo)

    return Response({
        'success': False,
        'message': 'Error interno del servidor.',
        'errors':  str(exc),
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
