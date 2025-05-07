import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Asegurate de que la fecha esté en formato datetime
ventas = pd.read_excel("caso_estudio_npi.xlsx", sheet_name="ventas")
ventas["fecha"] = pd.to_datetime(ventas["fecha"])

# Asegurarse de que las columnas estén correctas
print("Columnas:", ventas.columns.tolist())

# Asegurar formato de fecha
ventas["fecha"] = pd.to_datetime(ventas["fecha"], format="%m-%d-%Y", errors="coerce")

# Verificar valores nulos
if ventas["fecha"].isnull().any():
    print("⚠️ Hay fechas inválidas en el dataset")

# Contar ventas por producto
ventas_por_producto = ventas["producto"].value_counts().reset_index()
ventas_por_producto.columns = ["producto", "ventas_totales"]

# Filtrar productos con al menos 1 venta
productos_validos = ventas_por_producto[ventas_por_producto["ventas_totales"] > 0]["producto"]
ventas_filtradas = ventas[ventas["producto"].isin(productos_validos)]

# Agrupar por semana
ventas_filtradas["semana"] = ventas_filtradas["fecha"].dt.to_period("W").apply(lambda r: r.start_time)
ventas_por_semana = ventas_filtradas.groupby(["semana", "producto"]).size().reset_index(name="ventas")

# Gráfico
plt.figure(figsize=(12, 6))
sns.lineplot(data=ventas_por_semana, x="semana", y="ventas", hue="producto", marker="o")

# Línea de evento (opcional)
plt.axvline(pd.to_datetime("2024-03-15"), color="gray", linestyle="--", label="Lanzamiento A")

# Estética
plt.title("Ventas semanales por producto (solo con ventas reales)")
plt.xlabel("Semana")
plt.ylabel("Ventas")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()