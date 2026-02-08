import os   
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:8516203@localhost:5432/empresa_ventas")

os.makedirs("assets", exist_ok=True)

def ventas_mensuales(engine):

    #Análisis de ventas mensuales

    query = """ 
    SELECT
        DATE_TRUNC('month', fecha) AS mes,
        SUM(ingresos) AS total_ingresos
    FROM ventas
    GROUP BY mes
    ORDER BY mes;
    """ 
    df_mes = pd.read_sql_query(query, engine)
    plt.figure(figsize=(8, 4))
    plt.plot(df_mes['mes'], df_mes['total_ingresos'])
    plt.title('Ventas Mensuales')
    plt.xlabel('Mes')
    plt.ylabel('Ingresos') 
    plt.tight_layout()  
    plt.savefig('assets/ventas_mensuales.png')
    plt.close()


def productos_mas_vendidos(engine):

     #Productos más vendidos

    query = """
    SELECT
        producto_id,
        SUM(ingresos) AS total_ingresos
    FROM ventas
    GROUP BY producto_id
    ORDER BY total_ingresos DESC
    LIMIT 10;
    """
    df_productos = pd.read_sql_query(query, engine)
    plt.figure(figsize=(8, 4))
    df_productos.plot(kind='bar', x='producto_id', y='total_ingresos', legend=False)
    plt.title('Top 10 de productos Más Vendidos')
    plt.xlabel('Producto')
    plt.ylabel('Ingresos')
    plt.tight_layout()  
    plt.savefig('assets/productos_mas_vendidos.png')
    plt.close()


def top_clientes(engine):

    #Top 10 de clientes

    query = """
    SELECT
    cliente_id,
    SUM(ingresos) AS total_cliente
    FROM ventas
    GROUP BY cliente_id
    ORDER BY total_cliente DESC
    LIMIT 10;
    """
    df_clientes = pd.read_sql_query(query, engine)
    plt.figure(figsize=(8, 4))
    df_clientes.plot(kind='bar', x='cliente_id', y='total_cliente', legend=False)
    plt.title('Top 10 de Clientes')
    plt.xlabel('Cliente')
    plt.ylabel('Ingresos')
    plt.tight_layout()  
    plt.savefig('assets/top_clientes.png')
    plt.close()



def ventas_por_ciudad (engine):

    #Ventas por ciudad
    query = """
    SELECT
        c.ciudad,
        SUM(v.ingresos) AS total_ingresos
    FROM ventas v
    JOIN clientes c ON v.cliente_id = c.id
    GROUP BY c.ciudad
    ORDER BY total_ingresos DESC;
    """
    df_ciudad = pd.read_sql_query(query, engine)
    plt.figure(figsize=(8, 4))
    df_ciudad.plot(kind='bar', x='ciudad', y='total_ingresos', legend=False)
    plt.title('Ventas por Ciudad')
    plt.xlabel('Ciudad')
    plt.ylabel('Ingresos')
    plt.tight_layout()  
    plt.savefig('assets/ventas_por_ciudad.png')
    plt.close()

if __name__ == "__main__":
    ventas_mensuales(engine)
    productos_mas_vendidos(engine)
    top_clientes(engine)
    ventas_por_ciudad(engine)