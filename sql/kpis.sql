-- KPIs de negocio

-- KPI 1: Ingresos totales
SELECT
    SUM(ingresos) AS ingresos_totales
FROM ventas;

-- KPI 2: Ingreso promedio por venta
SELECT
    ROUND(AVG(ingresos), 2) AS ingreso_promedio
FROM ventas;

-- KPI 3: Rentabilidad total y promedio
SELECT
    SUM(margen) AS margen_total,
    ROUND(AVG(margen), 2) AS margen_promedio
FROM ventas;

-- KPI 4: Top 5 clientes por ingresos
SELECT
    cliente_id,
    SUM(ingresos) AS total_ingresos
FROM ventas
GROUP BY cliente_id
ORDER BY total_ingresos DESC
LIMIT 5;

-- KPI 5: Ingresos porcentuales por producto
SELECT
    producto_id,
    SUM(ingresos) AS total_producto,
    ROUND(
        SUM(ingresos) * 100.0 / (SELECT SUM(ingresos) FROM ventas),
        2
    ) AS porcentaje_ingresos
FROM ventas
GROUP BY producto_id
ORDER BY porcentaje_ingresos DESC;

-- KPI 6: Cliente más rentable
SELECT
    cliente_id,
    SUM(margen) AS margen_total
FROM ventas
GROUP BY cliente_id
ORDER BY margen_total DESC
LIMIT 1;
