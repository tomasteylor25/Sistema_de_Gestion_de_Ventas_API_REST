"""Paginación estándar del proyecto"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'message': 'Consulta exitosa',
            'data': data,
            'paginacion': {
                'total':          self.page.paginator.count,
                'pagina_actual':  self.page.number,
                'total_paginas':  self.page.paginator.num_pages,
                'siguiente':      self.get_next_link(),
                'anterior':       self.get_previous_link(),
                'por_pagina':     self.get_page_size(self.request),
            }
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'success':    {'type': 'boolean'},
                'message':    {'type': 'string'},
                'data':       schema,
                'paginacion': {
                    'type': 'object',
                    'properties': {
                        'total':         {'type': 'integer'},
                        'pagina_actual': {'type': 'integer'},
                        'total_paginas': {'type': 'integer'},
                        'siguiente':     {'type': 'string', 'nullable': True},
                        'anterior':      {'type': 'string', 'nullable': True},
                        'por_pagina':    {'type': 'integer'},
                    }
                }
            }
        }
