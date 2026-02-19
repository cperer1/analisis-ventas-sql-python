import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import random


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")

load_dotenv(env_path)

# Conexión a PostgreSQL
engine = create_engine(
    f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

# 1. Crear clientes
num_clientes = 5000
clientes = pd.DataFrame({
    "id": range(1, num_clientes + 1),
    "nombre": [f"Cliente_{i}" for i in range(1, num_clientes + 1)],
    "ciudad": np.random.choice(["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga"], num_clientes)
})

# 2. Crear productos
num_productos = 50
productos = pd.DataFrame({
    "id": range(1, num_productos + 1),
    "producto": [f"Producto_{i}" for i in range(1, num_productos + 1)],
    "precio": np.random.randint(20000, 500000, num_productos),
    "costo": np.random.randint(10000, 300000, num_productos)
})

# 3. Crear ventas
num_ventas = 100000
fechas = [datetime(2023,1,1) + timedelta(days=random.randint(0,730)) for _ in range(num_ventas)]

ventas = pd.DataFrame({
    "id": range(1, num_ventas + 1),
    "fecha": fechas,
    "cliente_id": np.random.randint(1, num_clientes+1, num_ventas),
    "producto_id": np.random.randint(1, num_productos+1, num_ventas),
    "cantidad": np.random.randint(1, 10, num_ventas)
})

ventas = ventas.merge(productos, left_on="producto_id", right_on="id")
ventas["ingresos"] = ventas["cantidad"] * ventas["precio"]
ventas["costos"] = ventas["cantidad"] * ventas["costo"]
ventas["margen"] = ventas["ingresos"] - ventas["costos"]

# 4. Cargar a PostgreSQL
clientes.to_sql("clientes", engine, if_exists="replace", index=False)
productos.to_sql("productos", engine, if_exists="replace", index=False)
ventas.to_sql("ventas", engine, if_exists="replace", index=False)

print("Base de datos generada con éxito: 100.000 ventas cargadas.")