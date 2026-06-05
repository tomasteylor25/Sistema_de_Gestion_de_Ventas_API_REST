-- ============================================================
-- SISTEMA DE GESTIÓN DE VENTAS
-- Script 04: Consultas de verificación y reportes
-- ============================================================

SET search_path TO ventas_schema, public;

-- ── 1. Resumen general de tablas ──────────────────────────────────────────────
SELECT tabla, registros FROM (
    SELECT 'clientes'       AS tabla, COUNT(*) AS registros FROM clientes
    UNION ALL SELECT 'proveedores',   COUNT(*) FROM proveedores
    UNION ALL SELECT 'sucursales',    COUNT(*) FROM sucursales
    UNION ALL SELECT 'productos',     COUNT(*) FROM productos
    UNION ALL SELECT 'pedidos',       COUNT(*) FROM pedidos
    UNION ALL SELECT 'detalle_pedidos', COUNT(*) FROM detalle_pedidos
    UNION ALL SELECT 'facturas',      COUNT(*) FROM facturas
    UNION ALL SELECT 'pagos',         COUNT(*) FROM pagos
) t ORDER BY tabla;

-- ── 2. Pedidos con cliente y sucursal ─────────────────────────────────────────
SELECT
    p.numero_pedido,
    p.fecha_pedido,
    p.estado,
    c.nombre || ' ' || c.apellido  AS cliente,
    s.nombre                        AS sucursal,
    p.total
FROM pedidos p
JOIN clientes   c ON c.id = p.cliente_id
JOIN sucursales s ON s.id = p.sucursal_id
ORDER BY p.fecha_pedido DESC;

-- ── 3. Detalle completo de un pedido ─────────────────────────────────────────
SELECT
    ped.numero_pedido,
    prod.nombre           AS producto,
    dp.cantidad,
    dp.precio_unitario,
    dp.descuento          AS "desc%",
    dp.subtotal
FROM detalle_pedidos dp
JOIN pedidos  ped  ON ped.id  = dp.pedido_id
JOIN productos prod ON prod.id = dp.producto_id
WHERE ped.numero_pedido = 'PED-2024-003'
ORDER BY prod.nombre;

-- ── 4. Facturas con estado de pago ───────────────────────────────────────────
SELECT
    f.numero_factura,
    f.fecha_emision,
    f.fecha_vencimiento,
    f.estado              AS estado_factura,
    f.total,
    COALESCE(SUM(pg.monto), 0)          AS total_pagado,
    f.total - COALESCE(SUM(pg.monto), 0) AS saldo_pendiente
FROM facturas f
LEFT JOIN pagos pg ON pg.factura_id = f.id AND pg.estado = 'APROBADO'
GROUP BY f.id, f.numero_factura, f.fecha_emision, f.fecha_vencimiento, f.estado, f.total
ORDER BY f.fecha_emision DESC;

-- ── 5. Productos con stock bajo ───────────────────────────────────────────────
SELECT
    p.codigo,
    p.nombre,
    p.stock,
    p.stock_minimo,
    pr.nombre AS proveedor
FROM productos p
JOIN proveedores pr ON pr.id = p.proveedor_id
WHERE p.stock <= p.stock_minimo AND p.activo = TRUE
ORDER BY p.stock ASC;

-- ── 6. Ventas por sucursal ────────────────────────────────────────────────────
SELECT
    s.nombre            AS sucursal,
    COUNT(p.id)         AS total_pedidos,
    SUM(p.total)        AS ventas_brutas
FROM pedidos p
JOIN sucursales s ON s.id = p.sucursal_id
WHERE p.activo = TRUE AND p.estado != 'CANCELADO'
GROUP BY s.id, s.nombre
ORDER BY ventas_brutas DESC;

-- ── 7. Top 5 productos más vendidos ──────────────────────────────────────────
SELECT
    prod.codigo,
    prod.nombre,
    SUM(dp.cantidad)   AS unidades_vendidas,
    SUM(dp.subtotal)   AS ingresos_totales
FROM detalle_pedidos dp
JOIN productos prod ON prod.id = dp.producto_id
JOIN pedidos   ped  ON ped.id  = dp.pedido_id
WHERE ped.estado != 'CANCELADO'
GROUP BY prod.id, prod.codigo, prod.nombre
ORDER BY unidades_vendidas DESC
LIMIT 5;

-- ── 8. Clientes eliminados (soft delete) ─────────────────────────────────────
SELECT id, tipo_documento, numero_documento, nombre, apellido, email
FROM clientes
WHERE activo = FALSE;

-- ── 9. Verificar relaciones (integridad referencial) ─────────────────────────
SELECT
    'Productos sin proveedor activo' AS verificacion,
    COUNT(*) AS total
FROM productos p
LEFT JOIN proveedores pr ON pr.id = p.proveedor_id AND pr.activo = TRUE
WHERE p.activo = TRUE AND pr.id IS NULL

UNION ALL

SELECT
    'Pedidos sin cliente activo',
    COUNT(*)
FROM pedidos p
LEFT JOIN clientes c ON c.id = p.cliente_id AND c.activo = TRUE
WHERE p.activo = TRUE AND c.id IS NULL

UNION ALL

SELECT
    'Facturas sin pedido',
    COUNT(*)
FROM facturas f
LEFT JOIN pedidos p ON p.id = f.pedido_id
WHERE f.activo = TRUE AND p.id IS NULL;
