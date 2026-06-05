"""
Script de datos de prueba para el Sistema de Gestión de Ventas.
Ejecutar con: python manage.py shell < docs/seed_data.py
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group
from api.clientes.models import Cliente
from api.proveedores.models import Proveedor
from api.sucursales.models import Sucursal
from api.productos.models import Producto
from api.pedidos.models import Pedido
from api.detalle_pedidos.models import DetallePedido
from api.facturas.models import Factura
from api.pagos.models import Pago
from datetime import date, timedelta
from decimal import Decimal

print("🌱 Iniciando seed de datos...")

# ── Grupos / Roles ────────────────────────────────────────────────────────────
for nombre in ['Administrador', 'Vendedor', 'Bodega']:
    Group.objects.get_or_create(name=nombre)
print("✅ Grupos creados")

# ── Superusuario (si no existe) ───────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ventas.com', 'Admin1234!')
    print("✅ Superusuario creado: admin / Admin1234!")

admin = User.objects.get(username='admin')

# ── Sucursales ────────────────────────────────────────────────────────────────
s1, _ = Sucursal.objects.get_or_create(codigo='SUC-BOG', defaults={
    'nombre': 'Sucursal Bogotá', 'direccion': 'Cra 7 # 32-16', 'ciudad': 'Bogotá',
    'telefono': '3001234567', 'email': 'bogota@ventas.com', 'es_principal': True,
    'creado_por': admin
})
s2, _ = Sucursal.objects.get_or_create(codigo='SUC-MED', defaults={
    'nombre': 'Sucursal Medellín', 'direccion': 'Calle 50 # 45-30', 'ciudad': 'Medellín',
    'telefono': '3109876543', 'email': 'medellin@ventas.com',
    'creado_por': admin
})
print("✅ Sucursales creadas")

# ── Proveedores ───────────────────────────────────────────────────────────────
p1, _ = Proveedor.objects.get_or_create(nit='900111222-1', defaults={
    'nombre': 'Distribuidora Tecno SAS', 'contacto': 'Carlos Ríos',
    'email': 'ventas@tecno.com', 'telefono': '3151112233', 'ciudad': 'Bogotá',
    'creado_por': admin
})
p2, _ = Proveedor.objects.get_or_create(nit='800333444-2', defaults={
    'nombre': 'Importaciones del Valle LTDA', 'contacto': 'Ana Gómez',
    'email': 'info@impvalle.com', 'telefono': '3204445566', 'ciudad': 'Cali',
    'creado_por': admin
})
print("✅ Proveedores creados")

# ── Productos ─────────────────────────────────────────────────────────────────
pr1, _ = Producto.objects.get_or_create(codigo='PROD-001', defaults={
    'nombre': 'Laptop Dell Inspiron 15', 'precio': Decimal('2800000'),
    'stock': 20, 'stock_minimo': 3, 'proveedor': p1, 'creado_por': admin
})
pr2, _ = Producto.objects.get_or_create(codigo='PROD-002', defaults={
    'nombre': 'Mouse Inalámbrico Logitech', 'precio': Decimal('85000'),
    'stock': 50, 'stock_minimo': 10, 'proveedor': p1, 'creado_por': admin
})
pr3, _ = Producto.objects.get_or_create(codigo='PROD-003', defaults={
    'nombre': 'Teclado Mecánico RGB', 'precio': Decimal('320000'),
    'stock': 15, 'stock_minimo': 5, 'proveedor': p2, 'creado_por': admin
})
print("✅ Productos creados")

# ── Clientes ──────────────────────────────────────────────────────────────────
c1, _ = Cliente.objects.get_or_create(numero_documento='1020304050', defaults={
    'tipo_documento': 'CC', 'nombre': 'María', 'apellido': 'López',
    'email': 'maria.lopez@email.com', 'telefono': '3112223344',
    'ciudad': 'Bogotá', 'creado_por': admin
})
c2, _ = Cliente.objects.get_or_create(numero_documento='900555666-3', defaults={
    'tipo_documento': 'NIT', 'nombre': 'TechCorp Colombia', 'apellido': '',
    'email': 'compras@techcorp.co', 'telefono': '6017778899',
    'ciudad': 'Bogotá', 'creado_por': admin
})
print("✅ Clientes creados")

# ── Pedido de prueba ──────────────────────────────────────────────────────────
ped, created = Pedido.objects.get_or_create(numero_pedido='PED-2024-001', defaults={
    'fecha_pedido': date.today(),
    'fecha_entrega': date.today() + timedelta(days=7),
    'estado': 'APROBADO',
    'cliente': c1,
    'sucursal': s1,
    'creado_por': admin
})

if created:
    DetallePedido.objects.create(
        pedido=ped, producto=pr1,
        cantidad=1, precio_unitario=Decimal('2800000'),
        descuento=Decimal('5'), creado_por=admin
    )
    DetallePedido.objects.create(
        pedido=ped, producto=pr2,
        cantidad=2, precio_unitario=Decimal('85000'),
        descuento=Decimal('0'), creado_por=admin
    )
    print("✅ Pedido y detalles creados")

# ── Factura de prueba ─────────────────────────────────────────────────────────
if not Factura.objects.filter(numero_factura='FAC-2024-001').exists():
    Factura.objects.create(
        numero_factura='FAC-2024-001',
        fecha_emision=date.today(),
        fecha_vencimiento=date.today() + timedelta(days=30),
        estado='PENDIENTE',
        pedido=ped,
        subtotal=ped.total,
        iva=Decimal('19'),
        creado_por=admin
    )
    print("✅ Factura creada")

fac = Factura.objects.get(numero_factura='FAC-2024-001')

# ── Pago de prueba ────────────────────────────────────────────────────────────
if not Pago.objects.filter(numero_pago='PAG-2024-001').exists():
    Pago.objects.create(
        numero_pago='PAG-2024-001',
        fecha_pago=date.today(),
        monto=fac.total,
        metodo_pago='TRANSFERENCIA',
        estado='APROBADO',
        referencia='TRF-987654321',
        factura=fac,
        creado_por=admin
    )
    print("✅ Pago creado")

print("\n🎉 Seed completado exitosamente.")
print("   Usuario: admin | Contraseña: Admin1234!")
print("   Swagger:  http://127.0.0.1:8000/api/docs/")
