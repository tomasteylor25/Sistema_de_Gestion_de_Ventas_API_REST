"""Middleware de logging para todas las peticiones HTTP"""

import logging
import time

logger = logging.getLogger('api')


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        inicio = time.time()

        usuario = (
            request.user.username
            if hasattr(request, 'user') and request.user.is_authenticated
            else 'Anónimo'
        )

        response = self.get_response(request)

        duracion_ms = round((time.time() - inicio) * 1000, 2)

        logger.info(
            f'{request.method} {request.path} | '
            f'Status: {response.status_code} | '
            f'Usuario: {usuario} | '
            f'IP: {self._get_ip(request)} | '
            f'Duración: {duracion_ms}ms'
        )

        return response

    @staticmethod
    def _get_ip(request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0]
        return request.META.get('REMOTE_ADDR', 'desconocida')
