import pandas as pd

# Cargar datos (asumimos que ya los tenés cargados con fechas correctas)
file_path = "caso_estudio_npi.xlsx"
productos = pd.read_excel(file_path, sheet_name="productos")
ventas = pd.read_excel(file_path, sheet_name="ventas")

ventas["fecha"] = pd.to_datetime(ventas["fecha"])
productos["fecha_lanzamiento"] = pd.to_datetime(productos["fecha_lanzamiento"])

# Inicializar resultados
resultados = []

for _, prod in productos.iterrows():
    producto_id = prod["id_producto"]
    nombre = prod["nombre"]
    lanzamiento = prod["fecha_lanzamiento"]
    
    ventana_inicio = lanzamiento - pd.DateOffset(months=3)
    ventana_fin = lanzamiento + pd.DateOffset(months=3)

    ventas_producto = ventas[ventas["producto"] ==producto_id]
    ventas_periodo = ventas_producto[
        (ventas_producto["fecha"] >= ventana_inicio) &
        (ventas_producto["fecha"] <= ventana_fin)
    ]

    ventas_periodo["fase"] = ventas_periodo["fecha"].apply(
        lambda x: "Pre" if x < lanzamiento else "Post"
    )

    resumen = ventas_periodo.groupby("fase")["cantidad"].sum().to_dict()

    resultados.append({
        "producto_id": producto_id,
        "nombre": nombre,
        "ventas_pre": resumen.get("Pre", 0),
        "ventas_post": resumen.get("Post", 0)
    })

# Convertimos a DataFrame
df_resultado = pd.DataFrame(resultados)

# Agregamos columna de diferencia
df_resultado["delta"] = df_resultado["ventas_post"] - df_resultado["ventas_pre"]

# Ordenamos por mayor impacto positivo
df_resultado = df_resultado.sort_values(by="delta", ascending=False)

print(df_resultado)

# Exportar a Excel
df_resultado.to_excel("impacto_npi_resultado.xlsx", index=False)

# También podés exportar a CSV si preferís
df_resultado.to_csv("impacto_npi_resultado.csv", index=False)

print("✅ Resultados guardados correctamente.")
print(ventas["producto"].unique())

