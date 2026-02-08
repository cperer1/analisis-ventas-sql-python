
-- 1. CONSULTA FRECUENTE SIN ÍNDICES
-- ¿Cómo se comporta una búsqueda por cliente y fecha?

EXPLAIN ANALYZE
SELECT *
FROM ventas
WHERE cliente_id = 2018
AND fecha BETWEEN '2023-01-01' AND '2023-12-31';
-- Mayor tiempo de ejecución

-- 2. CREACIÓN DE ÍNDICE
CREATE INDEX idx_ventas_cliente
ON ventas(cliente_id);

--Ejecutamos nuevamente 
EXPLAIN ANALYZE
SELECT *
FROM ventas
WHERE cliente_id = 2018
AND fecha BETWEEN '2023-01-01' AND '2023-12-31';
-- Reducción significativa del tiempo

-- 3. ÍNDICE COMPUESTO
-- Es más eficiente filtrar por cliente y fecha juntos
CREATE INDEX idx_ventas_cliente_fecha
ON ventas(cliente_id, fecha);

EXPLAIN ANALYZE
SELECT *
FROM ventas
WHERE cliente_id = 2018
AND fecha BETWEEN '2023-01-01' AND '2023-12-31';
-- Menos bloques leídos
-- Mejor rendimiento


-- 4. AGREGACIONES Y HASH AGGREGATE
-- ¿Cómo PostgreSQL agrupa grandes volúmenes de datos?
EXPLAIN ANALYZE
SELECT producto_id,
SUM(ingresos) AS total_ingresos
FROM ventas
GROUP BY producto_id;
-- HashAggregate
-- Uso eficiente de memoria

-- 5. VIEW VS CONSULTA DIRECTA
-- ¿Las vistas mejoran el rendimiento?
CREATE VIEW vw_ventas_completas AS
SELECT
v.fecha,
c.ciudad,
p.producto,
v.ingresos,
v.margen
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id
JOIN productos p ON v.producto_id = p.id;


EXPLAIN ANALYZE
SELECT *
FROM vw_ventas_completas
WHERE ciudad = 'Bogotá';
-- La vista no almacena datos
-- PostgreSQL consulta las tablas base


-- 6. MATERIALIZED VIEW PARA CONSULTAS REPETITIVAS
-- ¿Cómo acelerar consultas agregadas mensuales?
CREATE MATERIALIZED VIEW mv_ventas_mensuales AS
SELECT
DATE_TRUNC('month', fecha) AS mes,
SUM(ingresos) AS total_ingresos,
SUM(margen) AS total_margen
FROM ventas
GROUP BY mes;

EXPLAIN ANALYZE
SELECT *
FROM mv_ventas_mensuales;
-- Tiempo de ejecución muy bajo pero se debe actualizar cada vez que agreguemos datos 


