"""Permisos personalizados por rol para la API de Ventas"""

from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class EsAdministrador(BasePermission):
    """Solo usuarios del grupo Administrador."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.groups.filter(name='Administrador').exists()
            )
        )


class EsVendedor(BasePermission):
    """Solo usuarios del grupo Vendedor."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Vendedor').exists()
        )


class EsBodega(BasePermission):
    """Solo usuarios del grupo Bodega."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Bodega').exists()
        )


class AdminOVendedor(BasePermission):
    """Administrador o Vendedor."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser or
            request.user.groups.filter(name__in=['Administrador', 'Vendedor']).exists()
        )


class SoloLecturaOAdmin(BasePermission):
    """
    Cualquier autenticado puede leer (GET, HEAD, OPTIONS).
    Solo Administrador puede escribir (POST, PUT, PATCH, DELETE).
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_superuser or
            request.user.groups.filter(name='Administrador').exists()
        )
