--Exploración de datos

-- 1. Vista general de la tabla
SELECT *
FROM ventas
LIMIT 10;

-- 2. Ingresos totales
SELECT COUNT(*) AS total_registros
FROM ventas;

-- 3. Ventas mensuales
SELECT
    DATE_TRUNC('month', fecha) AS mes,
    SUM(ingresos) AS total_ingresos
FROM ventas
GROUP BY mes
ORDER BY mes;

-- 4. Ingresos por producto
SELECT
    producto_id,
    SUM(ingresos) AS total_ingresos
FROM ventas
GROUP BY producto_id
ORDER BY total_ingresos DESC;

-- 5. Ingresos por cliente
SELECT
    cliente_id,
    SUM(ingresos) AS total_cliente
FROM ventas
GROUP BY cliente_id
ORDER BY total_cliente DESC;

-- 6. Ventas por ciudad
SELECT
    c.ciudad,
    SUM(v.ingresos) AS total_ingresos
FROM ventas v
JOIN clientes c ON v.cliente_id = c.id
GROUP BY c.ciudad
ORDER BY total_ingresos DESC;



