"""
Comando: python manage.py setup_inicial
Crea los grupos de roles y el superusuario admin si no existen.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


ROLES = {
    'Administrador': '__all__',   # todos los permisos
    'Vendedor': [
        'view_cliente', 'add_cliente', 'change_cliente',
        'view_producto',
        'view_sucursal',
        'add_pedido', 'change_pedido', 'view_pedido',
        'add_detallepedido', 'change_detallepedido', 'view_detallepedido',
        'add_factura', 'view_factura',
        'add_pago', 'view_pago',
    ],
    'Bodega': [
        'view_producto', 'change_producto',
        'view_proveedor',
        'view_pedido',
        'view_detallepedido',
    ],
}


class Command(BaseCommand):
    help = 'Crea grupos de roles y superusuario inicial'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Configurando roles y usuario inicial...\n')

        # ── Grupos ────────────────────────────────────────────────────────────
        for nombre, permisos in ROLES.items():
            grupo, creado = Group.objects.get_or_create(name=nombre)
            if creado:
                self.stdout.write(f'  ✅ Grupo creado: {nombre}')
            else:
                self.stdout.write(f'  ⚡ Grupo ya existe: {nombre}')

            if permisos != '__all__' and creado:
                for codename in permisos:
                    try:
                        perm = Permission.objects.get(codename=codename)
                        grupo.permissions.add(perm)
                    except Permission.DoesNotExist:
                        pass  # Se asignan después de las migraciones

        # ── Superusuario ──────────────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@ventas.com',
                password='Admin1234!',
                first_name='Administrador',
                last_name='Sistema',
            )
            grupo_admin = Group.objects.get(name='Administrador')
            user.groups.add(grupo_admin)
            self.stdout.write(
                self.style.SUCCESS(
                    '\n  ✅ Superusuario creado:\n'
                    '     Usuario:    admin\n'
                    '     Contraseña: Admin1234!\n'
                    '     ⚠️  Cambia la contraseña en producción.'
                )
            )
        else:
            self.stdout.write('  ⚡ Superusuario "admin" ya existe')

        self.stdout.write(self.style.SUCCESS('\n🎉 Configuración inicial completada.'))
