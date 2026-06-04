# Sistema de Gestion de Ventas API REST
API REST para gestión de ventas desarrollada con Django. Incluye autenticación JWT, gestión de clientes y panel administrativo.

## Información General

| Campo | Detalle |
|---|---|
| **Nombre del proyecto** | Sistema de Gestión de Ventas |
| **Problema desarrollado** | Problema 4 — Guía de Aprendizaje CRUD Django/PostgreSQL |
| **Framework** | Django 4.2 + Django REST Framework 3.14 |
| **Base de datos** | PostgreSQL |
| **Autenticación** | JWT (JSON Web Tokens) |
| **Documentación** | Swagger / OpenAPI 3 |
| **Versión de API** | v1 (`/api/v1/`) |

---

## Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.10+ | Lenguaje principal |
| Django | 4.2.7 | Framework web |
| Django REST Framework | 3.14.0 | Construcción de la API |
| PostgreSQL | 14+ | Motor de base de datos |
| drf-spectacular | 0.26.5 | Documentación Swagger/OpenAPI |
| djangorestframework-simplejwt | 5.3.0 | Autenticación JWT |
| django-filter | 23.3 | Filtros avanzados |
| openpyxl | 3.1.2 | Exportación a Excel |
| python-dotenv / django-environ | 1.0.0 | Variables de entorno |

---

## Modelo de Datos

### Tablas implementadas (8)

| # | Tabla | Descripción |
|---|---|---|
| 1 | `clientes` | Clientes de la empresa |
| 2 | `productos` | Catálogo de productos |
| 3 | `proveedores` | Proveedores de productos |
| 4 | `pedidos` | Pedidos realizados por clientes |
| 5 | `detalle_pedidos` | Líneas de detalle de cada pedido |
| 6 | `facturas` | Facturas generadas por pedidos |
| 7 | `pagos` | Pagos realizados sobre facturas |
| 8 | `sucursales` | Sucursales de la empresa |

### Relaciones implementadas

```
Producto    ──►  Proveedor        (FK)
Pedido      ──►  Cliente          (FK)
Pedido      ──►  Sucursal         (FK)
DetallePedido ►  Pedido           (FK + CASCADE)
DetallePedido ►  Producto         (FK)
Factura     ──►  Pedido           (OneToOne)
Pago        ──►  Factura          (FK)
```

### Campos base en todas las tablas

Cada tabla hereda de `ModeloBase` e incluye:

| Campo | Tipo | Descripción |
|---|---|---|
| `activo` | Boolean | Soft delete |
| `fecha_creacion` | DateTimeField | Auto al crear |
| `fecha_modificacion` | DateTimeField | Auto al actualizar |
| `creado_por` | FK → User | Auditoría |
| `modificado_por` | FK → User | Auditoría |

---

## Ajustes Obligatorios Implementados (13/13)

| # | Ajuste | Implementación |
|---|---|---|
| 1 | Swagger | `drf-spectacular` → `/api/docs/` |
| 2 | Versionado de API | Prefijo `/api/v1/` |
| 3 | Respuestas JSON estandarizadas | `config/responses.py` |
| 4 | Paginación | `StandardPagination` en `config/pagination.py` |
| 5 | Filtros | `django-filter` + `FilterSet` por recurso |
| 6 | Ordenamiento | `OrderingFilter` de DRF |
| 7 | Soft Delete | `SoftDeleteMixin` → campo `activo=False` |
| 8 | Auditoría | `AuditoriaMixin` → `creado_por` / `modificado_por` |
| 9 | Autenticación JWT | `simplejwt` → `/api/v1/auth/` |
| 10 | Roles y permisos | `IsAuthenticated` + grupos de Django |
| 11 | Nested Serializers | Serializers anidados en Pedidos, Facturas, Pagos |
| 12 | Exportación Excel/CSV | Endpoint `/exportar/?formato=excel` o `csv` |
| 13 | Logging | `LoggingMiddleware` + `config/middleware.py` |

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ventas_api.git
cd ventas_api
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```env
DEBUG=****

DB_NAME=******
DB_USER=******
DB_PASSWORD=******
DB_HOST=******
DB_PORT=****
DB_SCHEMA=******
```

### 5. Crear la base de datos en PostgreSQL

```sql
-- En psql como superusuario:
CREATE DATABASE ventas_db;
\c ventas_db
CREATE SCHEMA ventas_schema;
```

### 6. Crear carpeta de logs

```bash
mkdir logs
```

### 7. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Crear superusuario

```bash
python manage.py createsuperuser
```

### 9. (Opcional) Crear grupos de roles

```bash
python manage.py shell
```
```python
from django.contrib.auth.models import Group
Group.objects.create(name='Administrador')
Group.objects.create(name='Vendedor')
Group.objects.create(name='Bodega')
```

---

## Ejecución

```bash
python manage.py runserver
```

El servidor arranca en: `http://127.0.0.1:8000`

---

## Documentación Swagger

Una vez el servidor está corriendo, accede a:

| URL | Descripción |
|---|---|
| `http://127.0.0.1:8000/api/docs/` | Swagger UI (interfaz interactiva) |
| `http://127.0.0.1:8000/api/redoc/` | ReDoc |
| `http://127.0.0.1:8000/api/schema/` | Esquema OpenAPI en JSON |

---

## Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/v1/auth/registro/` | Registrar usuario |
| POST | `/api/v1/auth/login/` | Iniciar sesión → obtener tokens JWT |
| POST | `/api/v1/auth/logout/` | Cerrar sesión (blacklist token) |
| GET  | `/api/v1/auth/perfil/` | Ver perfil del usuario autenticado |

### Recursos CRUD

Todos los recursos siguen el patrón estándar de DRF:

| Método | Endpoint | Descripción |
|---|---|---|
| GET    | `/api/v1/{recurso}/`            | Listar (con paginación, filtros y ordenamiento) |
| POST   | `/api/v1/{recurso}/`            | Crear |
| GET    | `/api/v1/{recurso}/{id}/`       | Ver detalle |
| PUT    | `/api/v1/{recurso}/{id}/`       | Actualizar completo |
| PATCH  | `/api/v1/{recurso}/{id}/`       | Actualizar parcial |
| DELETE | `/api/v1/{recurso}/{id}/`       | Soft Delete (`activo=False`) |
| GET    | `/api/v1/{recurso}/exportar/`   | Exportar Excel o CSV |

Recursos disponibles: `clientes`, `productos`, `proveedores`, `sucursales`, `pedidos`, `detalle-pedidos`, `facturas`, `pagos`

### Parámetros comunes de listado

| Parámetro | Ejemplo | Descripción |
|---|---|---|
| `page` | `?page=2` | Número de página |
| `page_size` | `?page_size=20` | Registros por página (máx. 100) |
| `search` | `?search=juan` | Búsqueda de texto |
| `ordering` | `?ordering=-fecha_creacion` | Ordenamiento |
| `activo` | `?activo=true` | Filtrar por estado activo |
| `formato` | `?formato=csv` | En `/exportar/`: `excel` o `csv` |

---

## Uso del JWT

### 1. Obtener token

```bash
POST /api/v1/auth/login/
{
  "username": "admin",
  "password": "tu_password"
}
```

Respuesta:
```json
{
  "success": true,
  "data": {
    "tokens": {
      "access":  "eyJ...",
      "refresh": "eyJ..."
    }
  }
}
```

### 2. Usar el token en cada petición

```
Authorization: Bearer eyJ...
```

---

## Estructura del Repositorio

```
ventas_api/
│
├── api/
│   ├── models_base.py          # Modelo abstracto base
│   ├── autenticacion/          # JWT: registro, login, logout
│   ├── clientes/               # CRUD Clientes
│   ├── productos/              # CRUD Productos
│   ├── proveedores/            # CRUD Proveedores
│   ├── sucursales/             # CRUD Sucursales
│   ├── pedidos/                # CRUD Pedidos
│   ├── detalle_pedidos/        # CRUD Detalle de Pedidos
│   ├── facturas/               # CRUD Facturas
│   └── pagos/                  # CRUD Pagos
│
├── config/
│   ├── settings.py             # Configuración Django
│   ├── urls.py                 # Rutas principales
│   ├── urls_v1.py              # Rutas versión 1
│   ├── pagination.py           # Paginación estandarizada
│   ├── responses.py            # Respuestas JSON uniformes
│   ├── exceptions.py           # Manejador de errores
│   ├── middleware.py           # Logging de peticiones
│   └── mixins.py               # Auditoría, SoftDelete, Respuestas
│
├── docs/
│   └── schema_postgresql.sql   # Script de referencia SQL
│
├── evidencias/                 # Capturas de pantalla
├── logs/                       # Archivos de log (generados en runtime)
│
├── .env.example                # Ejemplo de configuración
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## Git Flow

```
master   ──── versiones estables y finales (tags)
  │
develop  ──── desarrollo principal
  │
release  ──── versión candidata antes de pasar a master
```

### Comandos básicos

```bash
# Clonar y configurar ramas
git checkout -b develop
git checkout -b release

# Preparar release
git checkout -b release
git merge develop

# Pasar a master
git checkout master
git merge release
git tag -a v1.0.0 -m "Primera versión estable"
```

