-- ============================================================
-- SISTEMA DE GESTIÓN DE VENTAS
-- Script 02: Crear tablas
-- Ejecutar dentro de ventas_db con search_path = ventas_schema
-- ============================================================

SET search_path TO ventas_schema, public;

-- ============================================================
-- TABLA 1: clientes
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_schema.clientes (
    id                  BIGSERIAL       PRIMARY KEY,
    tipo_documento      VARCHAR(5)      NOT NULL
                            CHECK (tipo_documento IN ('CC','NIT','CE','PP')),
    numero_documento    VARCHAR(20)     NOT NULL UNIQUE,
    nombre              VARCHAR(150)    NOT NULL,
    apellido            VARCHAR(150)    NOT NULL DEFAULT '',
    email               VARCHAR(254)    NOT NULL UNIQUE,
    telefono            VARCHAR(20)     NOT NULL DEFAULT '',
    direccion           TEXT            NOT NULL DEFAULT '',
    ciudad              VARCHAR(100)    NOT NULL DEFAULT '',
    -- Campos base obligatorios
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    creado_por_id       INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL,
    modificado_por_id   INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL
);

COMMENT ON TABLE  ventas_schema.clientes IS 'Clientes de la empresa';
COMMENT ON COLUMN ventas_schema.clientes.activo IS 'FALSE = eliminado lógicamente (soft delete)';

-- ============================================================
-- TABLA 2: proveedores
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_schema.proveedores (
    id                  BIGSERIAL       PRIMARY KEY,
    nit                 VARCHAR(20)     NOT NULL UNIQUE,
    nombre              VARCHAR(200)    NOT NULL,
    contacto            VARCHAR(150)    NOT NULL DEFAULT '',
    email               VARCHAR(254)    NOT NULL DEFAULT '',
    telefono            VARCHAR(20)     NOT NULL DEFAULT '',
    direccion           TEXT            NOT NULL DEFAULT '',
    ciudad              VARCHAR(100)    NOT NULL DEFAULT '',
    sitio_web           VARCHAR(200)    NOT NULL DEFAULT '',
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    creado_por_id       INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL,
    modificado_por_id   INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL
);

COMMENT ON TABLE ventas_schema.proveedores IS 'Proveedores de productos';

-- ============================================================
-- TABLA 3: sucursales
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_schema.sucursales (
    id                  BIGSERIAL       PRIMARY KEY,
    codigo              VARCHAR(20)     NOT NULL UNIQUE,
    nombre              VARCHAR(200)    NOT NULL,
    direccion           TEXT            NOT NULL,
    ciudad              VARCHAR(100)    NOT NULL,
    telefono            VARCHAR(20)     NOT NULL DEFAULT '',
    email               VARCHAR(254)    NOT NULL DEFAULT '',
    es_principal        BOOLEAN         NOT NULL DEFAULT FALSE,
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    creado_por_id       INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL,
    modificado_por_id   INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL
);

COMMENT ON TABLE ventas_schema.sucursales IS 'Sucursales de la empresa';

-- ============================================================
-- TABLA 4: productos  (Relación → proveedores)
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_schema.productos (
    id                  BIGSERIAL       PRIMARY KEY,
    codigo              VARCHAR(50)     NOT NULL UNIQUE,
    nombre              VARCHAR(200)    NOT NULL,
    descripcion         TEXT            NOT NULL DEFAULT '',
    precio              NUMERIC(12,2)   NOT NULL CHECK (precio >= 0),
    stock               INTEGER         NOT NULL DEFAULT 0 CHECK (stock >= 0),
    stock_minimo        INTEGER         NOT NULL DEFAULT 5  CHECK (stock_minimo >= 0),
    unidad_medida       VARCHAR(5)      NOT NULL DEFAULT 'UND'
                            CHECK (unidad_medida IN ('UND','KG','LT','MT','CJ')),
    -- Relación: Producto → Proveedor
    proveedor_id        BIGINT          NOT NULL
                            REFERENCES ventas_schema.proveedores(id)
                            ON DELETE RESTRICT,
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    creado_por_id       INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL,
    modificado_por_id   INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL
);

COMMENT ON TABLE  ventas_schema.productos IS 'Catálogo de productos';
COMMENT ON COLUMN ventas_schema.productos.proveedor_id IS 'FK → proveedores (Producto → Proveedor)';

-- ============================================================
-- TABLA 5: pedidos  (Relaciones → clientes, sucursales)
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_schema.pedidos (
    id                  BIGSERIAL       PRIMARY KEY,
    numero_pedido       VARCHAR(20)     NOT NULL UNIQUE,
    fecha_pedido        DATE            NOT NULL,
    fecha_entrega       DATE,
    estado              VARCHAR(15)     NOT NULL DEFAULT 'PENDIENTE'
                            CHECK (estado IN ('PENDIENTE','APROBADO','ENVIADO','ENTREGADO','CANCELADO')),
    -- Relación: Pedido → Cliente
    cliente_id          BIGINT          NOT NULL
                            REFERENCES ventas_schema.clientes(id)
                            ON DELETE RESTRICT,
    -- Relación: Pedido → Sucursal
    sucursal_id         BIGINT          NOT NULL
                            REFERENCES ventas_schema.sucursales(id)
                            ON DELETE RESTRICT,
    observaciones       TEXT            NOT NULL DEFAULT '',
    total               NUMERIC(14,2)   NOT NULL DEFAULT 0 CHECK (total >= 0),
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    creado_por_id       INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL,
    modificado_por_id   INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL
);

COMMENT ON TABLE  ventas_schema.pedidos IS 'Pedidos realizados por clientes';
COMMENT ON COLUMN ventas_schema.pedidos.cliente_id   IS 'FK → clientes  (Pedido → Cliente)';
COMMENT ON COLUMN ventas_schema.pedidos.sucursal_id  IS 'FK → sucursales (Pedido → Sucursal)';
COMMENT ON COLUMN ventas_schema.pedidos.total        IS 'Calculado automáticamente desde detalle_pedidos';

-- ============================================================
-- TABLA 6: detalle_pedidos  (Relaciones → pedidos, productos)
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_schema.detalle_pedidos (
    id                  BIGSERIAL       PRIMARY KEY,
    -- Relación: DetallePedido → Pedido
    pedido_id           BIGINT          NOT NULL
                            REFERENCES ventas_schema.pedidos(id)
                            ON DELETE CASCADE,
    -- Relación: DetallePedido → Producto
    producto_id         BIGINT          NOT NULL
                            REFERENCES ventas_schema.productos(id)
                            ON DELETE RESTRICT,
    cantidad            INTEGER         NOT NULL CHECK (cantidad > 0),
    precio_unitario     NUMERIC(12,2)   NOT NULL CHECK (precio_unitario >= 0),
    descuento           NUMERIC(5,2)    NOT NULL DEFAULT 0
                            CHECK (descuento >= 0 AND descuento <= 100),
    subtotal            NUMERIC(14,2)   NOT NULL DEFAULT 0,
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    creado_por_id       INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL,
    modificado_por_id   INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL,
    -- Un producto no puede repetirse en el mismo pedido
    UNIQUE (pedido_id, producto_id)
);

COMMENT ON TABLE  ventas_schema.detalle_pedidos IS 'Líneas de detalle de cada pedido';
COMMENT ON COLUMN ventas_schema.detalle_pedidos.pedido_id   IS 'FK → pedidos   (DetallePedido → Pedido)';
COMMENT ON COLUMN ventas_schema.detalle_pedidos.producto_id IS 'FK → productos (DetallePedido → Producto)';
COMMENT ON COLUMN ventas_schema.detalle_pedidos.subtotal    IS 'cantidad * precio_unitario * (1 - descuento/100)';

-- ============================================================
-- TABLA 7: facturas  (Relación → pedidos)
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_schema.facturas (
    id                  BIGSERIAL       PRIMARY KEY,
    numero_factura      VARCHAR(20)     NOT NULL UNIQUE,
    fecha_emision       DATE            NOT NULL,
    fecha_vencimiento   DATE            NOT NULL,
    estado              VARCHAR(10)     NOT NULL DEFAULT 'PENDIENTE'
                            CHECK (estado IN ('PENDIENTE','PAGADA','ANULADA','VENCIDA')),
    -- Relación: Factura → Pedido (OneToOne)
    pedido_id           BIGINT          NOT NULL UNIQUE
                            REFERENCES ventas_schema.pedidos(id)
                            ON DELETE RESTRICT,
    subtotal            NUMERIC(14,2)   NOT NULL CHECK (subtotal >= 0),
    iva                 NUMERIC(5,2)    NOT NULL DEFAULT 19,
    total               NUMERIC(14,2)   NOT NULL CHECK (total >= 0),
    observaciones       TEXT            NOT NULL DEFAULT '',
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    creado_por_id       INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL,
    modificado_por_id   INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL
);

COMMENT ON TABLE  ventas_schema.facturas IS 'Facturas generadas por pedidos';
COMMENT ON COLUMN ventas_schema.facturas.pedido_id IS 'FK → pedidos (Factura → Pedido, relación 1:1)';
COMMENT ON COLUMN ventas_schema.facturas.total     IS 'subtotal * (1 + iva/100)';

-- ============================================================
-- TABLA 8: pagos  (Relación → facturas)
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas_schema.pagos (
    id                  BIGSERIAL       PRIMARY KEY,
    numero_pago         VARCHAR(20)     NOT NULL UNIQUE,
    fecha_pago          DATE            NOT NULL,
    monto               NUMERIC(14,2)   NOT NULL CHECK (monto > 0),
    metodo_pago         VARCHAR(15)     NOT NULL
                            CHECK (metodo_pago IN
                                ('EFECTIVO','TRANSFERENCIA','TARJETA_CRED',
                                'TARJETA_DEB','CHEQUE','PSE')),
    estado              VARCHAR(12)     NOT NULL DEFAULT 'PENDIENTE'
                            CHECK (estado IN ('PENDIENTE','APROBADO','RECHAZADO','REEMBOLSADO')),
    referencia          VARCHAR(100)    NOT NULL DEFAULT '',
    -- Relación: Pago → Factura
    factura_id          BIGINT          NOT NULL
                            REFERENCES ventas_schema.facturas(id)
                            ON DELETE RESTRICT,
    observaciones       TEXT            NOT NULL DEFAULT '',
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    creado_por_id       INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL,
    modificado_por_id   INTEGER         REFERENCES auth_user(id) ON DELETE SET NULL
);

COMMENT ON TABLE  ventas_schema.pagos IS 'Pagos realizados sobre facturas';
COMMENT ON COLUMN ventas_schema.pagos.factura_id IS 'FK → facturas (Pago → Factura)';

-- ============================================================
-- ÍNDICES para mejorar rendimiento
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_cli_email        ON ventas_schema.clientes(email);
CREATE INDEX IF NOT EXISTS idx_cli_documento    ON ventas_schema.clientes(numero_documento);
CREATE INDEX IF NOT EXISTS idx_cli_activo       ON ventas_schema.clientes(activo);

CREATE INDEX IF NOT EXISTS idx_pro_proveedor    ON ventas_schema.productos(proveedor_id);
CREATE INDEX IF NOT EXISTS idx_pro_activo       ON ventas_schema.productos(activo);

CREATE INDEX IF NOT EXISTS idx_ped_cliente      ON ventas_schema.pedidos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_ped_sucursal     ON ventas_schema.pedidos(sucursal_id);
CREATE INDEX IF NOT EXISTS idx_ped_estado       ON ventas_schema.pedidos(estado);
CREATE INDEX IF NOT EXISTS idx_ped_fecha        ON ventas_schema.pedidos(fecha_pedido);

CREATE INDEX IF NOT EXISTS idx_det_pedido       ON ventas_schema.detalle_pedidos(pedido_id);
CREATE INDEX IF NOT EXISTS idx_det_producto     ON ventas_schema.detalle_pedidos(producto_id);

CREATE INDEX IF NOT EXISTS idx_fac_pedido       ON ventas_schema.facturas(pedido_id);
CREATE INDEX IF NOT EXISTS idx_fac_estado       ON ventas_schema.facturas(estado);

CREATE INDEX IF NOT EXISTS idx_pag_factura      ON ventas_schema.pagos(factura_id);
CREATE INDEX IF NOT EXISTS idx_pag_estado       ON ventas_schema.pagos(estado);

-- ============================================================
-- TRIGGER: actualizar fecha_modificacion automáticamente
-- ============================================================
CREATE OR REPLACE FUNCTION ventas_schema.actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_modificacion = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a todas las tablas
DO $$
DECLARE
    t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY[
        'clientes','proveedores','sucursales','productos',
        'pedidos','detalle_pedidos','facturas','pagos'
    ] LOOP
        EXECUTE format(
            'CREATE OR REPLACE TRIGGER trg_%s_mod
            BEFORE UPDATE ON ventas_schema.%s
            FOR EACH ROW EXECUTE FUNCTION ventas_schema.actualizar_fecha_modificacion();',
            t, t
        );
    END LOOP;
END;
$$;

SELECT 'Tablas, índices y triggers creados correctamente.' AS resultado;
