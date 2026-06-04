-- ============================================================
-- SISTEMA DE GESTIÓN DE VENTAS
-- Script 01: Crear base de datos y schema
-- Ejecutar como superusuario de PostgreSQL
-- ============================================================

-- Crear la base de datos
CREATE DATABASE ventas_db
    WITH ENCODING = 'UTF8'
    LC_COLLATE = 'es_CO.UTF-8'
    LC_CTYPE   = 'es_CO.UTF-8'
    TEMPLATE   = template0;

-- Conectarse a ventas_db antes de continuar:
-- \c ventas_db

-- Crear schema
CREATE SCHEMA IF NOT EXISTS ventas_schema;

-- Establecer schema por defecto
SET search_path TO ventas_schema, public;

-- Crear usuario de aplicación
CREATE USER ventas_user WITH PASSWORD 'VentasPass2024!';
GRANT USAGE  ON SCHEMA ventas_schema TO ventas_user;
GRANT CREATE ON SCHEMA ventas_schema TO ventas_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ventas_schema
    GRANT ALL PRIVILEGES ON TABLES    TO ventas_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ventas_schema
    GRANT ALL PRIVILEGES ON SEQUENCES TO ventas_user;

SELECT 'Base de datos y schema creados correctamente.' AS resultado;
