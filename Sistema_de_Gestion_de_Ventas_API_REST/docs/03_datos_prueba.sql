-- ============================================================
-- SISTEMA DE GESTIÓN DE VENTAS
-- Script 03: Datos de prueba (INSERT)
-- Ejecutar DESPUÉS del script 02
-- ============================================================

SET search_path TO ventas_schema, public;

-- ============================================================
-- SUCURSALES
-- ============================================================
INSERT INTO ventas_schema.sucursales
    (codigo, nombre, direccion, ciudad, telefono, email, es_principal, activo)
VALUES
    ('SUC-BOG', 'Sucursal Bogotá Principal',  'Cra 7 # 32-16, Centro',         'Bogotá',      '6017001122', 'bogota@ventas.com',    TRUE,  TRUE),
    ('SUC-MED', 'Sucursal Medellín',          'Calle 50 # 45-30, El Poblado',  'Medellín',    '6044452233', 'medellin@ventas.com',  FALSE, TRUE),
    ('SUC-CAL', 'Sucursal Cali',              'Av 6N # 23-45, Granada',        'Cali',        '6023456789', 'cali@ventas.com',      FALSE, TRUE),
    ('SUC-BAR', 'Sucursal Barranquilla',      'Cra 43 # 84-110, El Prado',     'Barranquilla','6053217890', 'barranquilla@ventas.com', FALSE, TRUE)
ON CONFLICT DO NOTHING;

-- ============================================================
-- PROVEEDORES
-- ============================================================
INSERT INTO ventas_schema.proveedores
    (nit, nombre, contacto, email, telefono, ciudad, sitio_web, activo)
VALUES
    ('900111222-1', 'Distribuidora Tecno SAS',        'Carlos Ríos',       'ventas@tecno.com',        '3151112233', 'Bogotá',   'www.tecno.com',       TRUE),
    ('800333444-2', 'Importaciones del Valle LTDA',   'Ana Gómez',         'info@impvalle.com',       '3204445566', 'Cali',     'www.impvalle.com',    TRUE),
    ('900777888-3', 'Electrónicos del Norte SAS',     'Pedro Martínez',    'pedidos@elnorte.com',     '3107778899', 'Medellín', 'www.elnorte.com',     TRUE),
    ('700555666-4', 'Suministros Industriales SA',    'Laura Herrera',     'compras@suministros.co',  '6014443355', 'Bogotá',   'www.suministros.co',  TRUE),
    ('901234567-5', 'Tech Import Colombia LTDA',      'Diego Vargas',      'dvargas@techimport.co',   '3209876543', 'Bogotá',   'www.techimport.co',   FALSE)
ON CONFLICT DO NOTHING;

-- ============================================================
-- CLIENTES
-- ============================================================
INSERT INTO ventas_schema.clientes
    (tipo_documento, numero_documento, nombre, apellido, email, telefono, ciudad, activo)
VALUES
    ('CC',  '1020304050', 'María',          'López Ruiz',       'maria.lopez@email.com',      '3112223344', 'Bogotá',      TRUE),
    ('CC',  '1031456789', 'Juan Carlos',    'Pérez García',     'jcperez@email.com',          '3223334455', 'Medellín',    TRUE),
    ('NIT', '900555666-3','TechCorp Colombia SAS', '',           'compras@techcorp.co',        '6017778899', 'Bogotá',      TRUE),
    ('CC',  '52789012',   'Sandra',         'Morales Vega',     'sandra.morales@gmail.com',   '3134445566', 'Cali',        TRUE),
    ('CE',  'CE123456',   'James',          'Wilson',           'jwilson@company.com',        '3209876543', 'Bogotá',      TRUE),
    ('NIT', '800987654-1','Inversiones ABC LTDA', '',           'gerencia@inversionesabc.co', '6044561234', 'Medellín',    TRUE),
    ('CC',  '79345678',   'Roberto',        'Castro Niño',      'roberto.castro@hotmail.com', '3005556677', 'Barranquilla',TRUE),
    ('PP',  'PP987654',   'Sophie',         'Dupont',           'sdupont@mail.fr',            '3118889900', 'Bogotá',      TRUE),
    ('CC',  '1098765432', 'Valentina',      'Torres Ospina',    'vtorres@email.co',           '3201112233', 'Cali',        FALSE),
    ('NIT', '901122334-2','Comercializadora XYZ','',            'pedidos@xyz.com.co',         '6013344556', 'Bogotá',      TRUE)
ON CONFLICT DO NOTHING;

-- ============================================================
-- PRODUCTOS  (referenciando proveedores por nit)
-- ============================================================
INSERT INTO ventas_schema.productos
    (codigo, nombre, descripcion, precio, stock, stock_minimo, unidad_medida, proveedor_id, activo)
SELECT
    p.codigo, p.nombre, p.descripcion, p.precio, p.stock, p.stock_minimo, p.unidad_medida,
    pr.id, TRUE
FROM (VALUES
    ('PROD-001', 'Laptop Dell Inspiron 15',       'Procesador i5, 8GB RAM, 512GB SSD',     2800000.00, 20,  3, 'UND', '900111222-1'),
    ('PROD-002', 'Mouse Inalámbrico Logitech M185','Receptor USB, 1000 DPI, Negro',            85000.00, 50, 10, 'UND', '900111222-1'),
    ('PROD-003', 'Teclado Mecánico RGB HyperX',   'Switch Blue, retroiluminación RGB',       320000.00, 15,  5, 'UND', '800333444-2'),
    ('PROD-004', 'Monitor Samsung 24" FHD',       'Panel IPS, 75Hz, HDMI, VGA',            950000.00, 10,  2, 'UND', '900777888-3'),
    ('PROD-005', 'Disco SSD Kingston 1TB',        'SATA III, 550MB/s lectura',              380000.00, 30,  5, 'UND', '800333444-2'),
    ('PROD-006', 'Cable HDMI 2.0 3m',             'Resolución 4K, trenzado',                 28000.00, 100, 20, 'UND', '700555666-4'),
    ('PROD-007', 'UPS CDP 1000VA',                'Regulador de voltaje, 6 tomas',          420000.00,  8,  2, 'UND', '700555666-4'),
    ('PROD-008', 'Audífonos Sony WH-1000XM5',     'Cancelación de ruido activa, Bluetooth', 890000.00, 12,  3, 'UND', '900777888-3'),
    ('PROD-009', 'Webcam Logitech C920',          '1080p Full HD, micrófono integrado',     310000.00, 18,  4, 'UND', '900111222-1'),
    ('PROD-010', 'Router WiFi TP-Link Archer AX73','WiFi 6, AX5400, doble banda',           590000.00,  6,  2, 'UND', '900777888-3')
) AS p(codigo, nombre, descripcion, precio, stock, stock_minimo, unidad_medida, prov_nit)
JOIN ventas_schema.proveedores pr ON pr.nit = p.prov_nit
ON CONFLICT DO NOTHING;

-- ============================================================
-- PEDIDOS (referenciando clientes y sucursales)
-- ============================================================
INSERT INTO ventas_schema.pedidos
    (numero_pedido, fecha_pedido, fecha_entrega, estado, cliente_id, sucursal_id, observaciones, total)
SELECT
    p.numero_pedido, p.fecha_pedido::DATE, p.fecha_entrega::DATE, p.estado,
    c.id, s.id, p.observaciones, 0
FROM (VALUES
    ('PED-2024-001', '2024-01-10', '2024-01-17', 'ENTREGADO', '1020304050',  'SUC-BOG', 'Entrega en oficina'),
    ('PED-2024-002', '2024-01-15', '2024-01-22', 'ENTREGADO', '1031456789',  'SUC-MED', ''),
    ('PED-2024-003', '2024-02-01', '2024-02-08', 'ENTREGADO', '900555666-3', 'SUC-BOG', 'Factura a nombre de la empresa'),
    ('PED-2024-004', '2024-02-14', '2024-02-21', 'ENVIADO',   '52789012',    'SUC-CAL', ''),
    ('PED-2024-005', '2024-03-05', '2024-03-12', 'APROBADO',  'CE123456',    'SUC-BOG', 'Cliente extranjero'),
    ('PED-2024-006', '2024-03-20', NULL,          'CANCELADO', '79345678',    'SUC-BAR', 'Cancelado por el cliente'),
    ('PED-2024-007', '2024-04-02', '2024-04-09', 'PENDIENTE', '800987654-1', 'SUC-MED', 'Requiere factura electrónica'),
    ('PED-2024-008', '2024-04-18', '2024-04-25', 'APROBADO',  '901122334-2', 'SUC-BOG', '')
) AS p(numero_pedido, fecha_pedido, fecha_entrega, estado, cli_doc, suc_cod, observaciones)
JOIN ventas_schema.clientes   c ON c.numero_documento = p.cli_doc
JOIN ventas_schema.sucursales s ON s.codigo           = p.suc_cod
ON CONFLICT DO NOTHING;

-- ============================================================
-- DETALLE PEDIDOS
-- ============================================================
INSERT INTO ventas_schema.detalle_pedidos
    (pedido_id, producto_id, cantidad, precio_unitario, descuento, subtotal)
SELECT
    ped.id, prod.id, d.cantidad, d.precio_unitario, d.descuento,
    d.cantidad * d.precio_unitario * (1 - d.descuento / 100.0)
FROM (VALUES
    ('PED-2024-001', 'PROD-001', 1,  2800000.00, 5.00),
    ('PED-2024-001', 'PROD-002', 2,    85000.00, 0.00),
    ('PED-2024-002', 'PROD-003', 1,   320000.00, 0.00),
    ('PED-2024-002', 'PROD-004', 1,   950000.00, 3.00),
    ('PED-2024-003', 'PROD-001', 3,  2800000.00, 10.00),
    ('PED-2024-003', 'PROD-005', 3,   380000.00, 5.00),
    ('PED-2024-003', 'PROD-006', 5,    28000.00, 0.00),
    ('PED-2024-004', 'PROD-008', 2,   890000.00, 0.00),
    ('PED-2024-004', 'PROD-009', 1,   310000.00, 0.00),
    ('PED-2024-005', 'PROD-007', 2,   420000.00, 0.00),
    ('PED-2024-005', 'PROD-010', 1,   590000.00, 5.00),
    ('PED-2024-007', 'PROD-001', 2,  2800000.00, 8.00),
    ('PED-2024-007', 'PROD-004', 2,   950000.00, 5.00),
    ('PED-2024-008', 'PROD-001', 5,  2800000.00, 12.00),
    ('PED-2024-008', 'PROD-006', 10,   28000.00, 0.00)
) AS d(ped_num, prod_cod, cantidad, precio_unitario, descuento)
JOIN ventas_schema.pedidos   ped  ON ped.numero_pedido = d.ped_num
JOIN ventas_schema.productos prod ON prod.codigo        = d.prod_cod
ON CONFLICT DO NOTHING;

-- Actualizar totales en pedidos
UPDATE ventas_schema.pedidos p
SET total = (
    SELECT COALESCE(SUM(subtotal), 0)
    FROM ventas_schema.detalle_pedidos
    WHERE pedido_id = p.id
);

-- ============================================================
-- FACTURAS
-- ============================================================
INSERT INTO ventas_schema.facturas
    (numero_factura, fecha_emision, fecha_vencimiento, estado, pedido_id, subtotal, iva, total)
SELECT
    f.numero_factura,
    f.fecha_emision::DATE,
    f.fecha_vencimiento::DATE,
    f.estado,
    ped.id,
    ped.total,
    19.00,
    ped.total * 1.19
FROM (VALUES
    ('FAC-2024-001', '2024-01-10', '2024-02-10', 'PAGADA',    'PED-2024-001'),
    ('FAC-2024-002', '2024-01-15', '2024-02-15', 'PAGADA',    'PED-2024-002'),
    ('FAC-2024-003', '2024-02-01', '2024-03-01', 'PAGADA',    'PED-2024-003'),
    ('FAC-2024-004', '2024-02-14', '2024-03-14', 'PENDIENTE', 'PED-2024-004'),
    ('FAC-2024-005', '2024-03-05', '2024-04-05', 'PENDIENTE', 'PED-2024-005'),
    ('FAC-2024-007', '2024-04-02', '2024-05-02', 'PENDIENTE', 'PED-2024-007'),
    ('FAC-2024-008', '2024-04-18', '2024-05-18', 'PENDIENTE', 'PED-2024-008')
) AS f(numero_factura, fecha_emision, fecha_vencimiento, estado, ped_num)
JOIN ventas_schema.pedidos ped ON ped.numero_pedido = f.ped_num
ON CONFLICT DO NOTHING;

-- ============================================================
-- PAGOS
-- ============================================================
INSERT INTO ventas_schema.pagos
    (numero_pago, fecha_pago, monto, metodo_pago, estado, referencia, factura_id)
SELECT
    pg.numero_pago,
    pg.fecha_pago::DATE,
    fac.total,
    pg.metodo_pago,
    pg.estado,
    pg.referencia,
    fac.id
FROM (VALUES
    ('PAG-2024-001', '2024-01-12', 'FAC-2024-001', 'TRANSFERENCIA', 'APROBADO', 'TRF-100001'),
    ('PAG-2024-002', '2024-01-18', 'FAC-2024-002', 'TARJETA_CRED',  'APROBADO', 'VIS-200002'),
    ('PAG-2024-003', '2024-02-05', 'FAC-2024-003', 'PSE',           'APROBADO', 'PSE-300003'),
    ('PAG-2024-004', '2024-03-10', 'FAC-2024-004', 'EFECTIVO',      'PENDIENTE',''),
    ('PAG-2024-005', '2024-03-08', 'FAC-2024-005', 'TRANSFERENCIA', 'PENDIENTE','TRF-500005')
) AS pg(numero_pago, fecha_pago, fac_num, metodo_pago, estado, referencia)
JOIN ventas_schema.facturas fac ON fac.numero_factura = pg.fac_num
ON CONFLICT DO NOTHING;

SELECT 'Datos de prueba insertados correctamente.' AS resultado;

-- ============================================================
-- CONSULTAS DE VERIFICACIÓN
-- ============================================================
SELECT 'sucursales'     AS tabla, COUNT(*) AS registros FROM ventas_schema.sucursales
UNION ALL
SELECT 'proveedores',   COUNT(*) FROM ventas_schema.proveedores
UNION ALL
SELECT 'clientes',      COUNT(*) FROM ventas_schema.clientes
UNION ALL
SELECT 'productos',     COUNT(*) FROM ventas_schema.productos
UNION ALL
SELECT 'pedidos',       COUNT(*) FROM ventas_schema.pedidos
UNION ALL
SELECT 'detalle_pedidos', COUNT(*) FROM ventas_schema.detalle_pedidos
UNION ALL
SELECT 'facturas',      COUNT(*) FROM ventas_schema.facturas
UNION ALL
SELECT 'pagos',         COUNT(*) FROM ventas_schema.pagos
ORDER BY tabla;
