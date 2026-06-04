"""Respuestas JSON estandarizadas para toda la API"""

from rest_framework.response import Response
from rest_framework import status


def respuesta_exitosa(data=None, mensaje='Operación exitosa', codigo=status.HTTP_200_OK):
    return Response({
        'success': True,
        'message': mensaje,
        'data':    data,
    }, status=codigo)


def respuesta_creada(data=None, mensaje='Registro creado exitosamente'):
    return Response({
        'success': True,
        'message': mensaje,
        'data':    data,
    }, status=status.HTTP_201_CREATED)


def respuesta_error(mensaje='Error en la operación', errores=None, codigo=status.HTTP_400_BAD_REQUEST):
    return Response({
        'success': False,
        'message': mensaje,
        'errors':  errores,
    }, status=codigo)


def respuesta_no_encontrado(mensaje='Registro no encontrado'):
    return Response({
        'success': False,
        'message': mensaje,
        'data':    None,
    }, status=status.HTTP_404_NOT_FOUND)


def respuesta_eliminado(mensaje='Registro eliminado correctamente'):
    return Response({
        'success': True,
        'message': mensaje,
        'data':    None,
    }, status=status.HTTP_200_OK)
