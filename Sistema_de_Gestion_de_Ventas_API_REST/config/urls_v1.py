"""URLs versión 1 de la API"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.autenticacion.views import RegistroView, LoginView, LogoutView, PerfilView
from api.clientes.views import ClienteViewSet
from api.productos.views import ProductoViewSet
from api.proveedores.views import ProveedorViewSet
from api.sucursales.views import SucursalViewSet
from api.pedidos.views import PedidoViewSet
from api.detalle_pedidos.views import DetallePedidoViewSet
from api.facturas.views import FacturaViewSet
from api.pagos.views import PagoViewSet

router = DefaultRouter()
router.register(r'clientes',        ClienteViewSet,       basename='clientes')
router.register(r'productos',       ProductoViewSet,      basename='productos')
router.register(r'proveedores',     ProveedorViewSet,     basename='proveedores')
router.register(r'sucursales',      SucursalViewSet,      basename='sucursales')
router.register(r'pedidos',         PedidoViewSet,        basename='pedidos')
router.register(r'detalle-pedidos', DetallePedidoViewSet, basename='detalle-pedidos')
router.register(r'facturas',        FacturaViewSet,       basename='facturas')
router.register(r'pagos',           PagoViewSet,          basename='pagos')

urlpatterns = [
    # Autenticación
    path('auth/registro/', RegistroView.as_view(),  name='registro'),
    path('auth/login/',    LoginView.as_view(),     name='login'),
    path('auth/logout/',   LogoutView.as_view(),    name='logout'),
    path('auth/perfil/',   PerfilView.as_view(),    name='perfil'),

    # Recursos CRUD
    path('', include(router.urls)),
]
