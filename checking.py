import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Paso 1: Cargar los datos
productos = pd.read_excel("caso_estudio_npi.xlsx", sheet_name="productos")
ventas = pd.read_excel("caso_estudio_npi.xlsx", sheet_name="ventas")

# Paso 2: Limpiar y preparar los datos
ventas["fecha"] = pd.to_datetime(ventas["fecha"])  # aseguramos formato de fecha

# 🚀 NUEVO: unir productos con ventas por nombre
ventas = ventas.merge(productos[["id_producto", "nombre"]], left_on="producto", right_on="nombre", how="left")

# Paso 3: Crear DataFrame para resultados
resultados = []

# Paso 4: Analizar cada producto
for idx, row in productos.iterrows():
    producto_id = row["id_producto"]
    nombre = row["nombre"]
    lanzamiento = pd.to_datetime(row["fecha_lanzamiento"])

    # Filtramos ventas del producto
    ventas_producto = ventas[ventas["id_producto"] == producto_id]

    # Definimos ventanas de análisis (3 meses antes y después)
    fecha_pre = lanzamiento - pd.DateOffset(months=3)
    fecha_post = lanzamiento + pd.DateOffset(months=3)

    # Ventas antes y después del lanzamiento
    ventas_pre = ventas_producto[(ventas_producto["fecha"] >= fecha_pre) & (ventas_producto["fecha"] < lanzamiento)]
    ventas_post = ventas_producto[(ventas_producto["fecha"] >= lanzamiento) & (ventas_producto["fecha"] < fecha_post)]

    # 💡 Diagnóstico
    print(f"🔍 {nombre} ({producto_id})")
    print(f"  Ventas PRE: {ventas_pre.shape[0]}, POST: {ventas_post.shape[0]}")
    print("-" * 30)

    # Agregar al resumen
    resultados.append({
        "id_producto": producto_id,
        "nombre": nombre,
        "ventas_pre": ventas_pre.shape[0],
        "ventas_post": ventas_post.shape[0],
        "delta": ventas_post.shape[0] - ventas_pre.shape[0]
    })

# Paso 5: Crear DataFrame con resultados
df_resultados = pd.DataFrame(resultados)
print("\n📊 Resultado final:")
print(df_resultados)

# (Opcional) Exportar
df_resultados.to_csv("impacto_NPI.csv", index=False)

# Estilo visual
sns.set(style="whitegrid")

# Crear gráfico
plt.figure(figsize=(10, 6))
df_melt = df_resultados.melt(id_vars=["nombre"], value_vars=["ventas_pre", "ventas_post"], 
                              var_name="Periodo", value_name="Ventas")

# Gráfico de barras agrupadas
sns.barplot(data=df_melt, x="nombre", y="Ventas", hue="Periodo", palette="Set2")

# Títulos y etiquetas
plt.title("Impacto de Lanzamiento por Producto (Pre vs Post)", fontsize=14)
plt.xlabel("Producto")
plt.ylabel("Cantidad de Ventas")
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar
plt.show()