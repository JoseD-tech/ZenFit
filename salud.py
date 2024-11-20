import polars as pl
import pygal

# Cargar el archivo CSV
archivo = pl.read_csv('dataset-salud.csv')

# Renombrar columnas para facilitar el acceso
archivo = archivo.rename({
    'Fecha': 'Date',
    'Sexo': 'SX',
    'Edad': 'ED',
    'Pasos diarios': 'PS',
    'Calorías quemadas': 'CQ',
    'Horas de sueño': 'HS',
    'Calidad del sueño': 'CS',
    'Frecuencia cardíaca promedio': 'FCP',
    'Nivel de estrés': 'NE',
    'Estado de ánimo': 'EA'
})

# Seleccionar columnas relevantes para el análisis
archivo = archivo.select(['SX', 'FCP', 'NE', 'CQ', 'PS'])

# Cálculos de Correlación entre Nivel de Estrés y otras variables físicas
correlacion_estres_fcp = archivo.select(pl.corr("NE", "FCP")).item(0, 0)
correlacion_estres_ps = archivo.select(pl.corr("NE", "PS")).item(0, 0)
correlacion_estres_cq = archivo.select(pl.corr("NE", "CQ")).item(0, 0)

print("Coeficiente de correlación entre Nivel de Estrés y Frecuencia Cardíaca Promedio:", correlacion_estres_fcp)
print("Coeficiente de correlación entre Nivel de Estrés y Pasos Diarios:", correlacion_estres_ps)
print("Coeficiente de correlación entre Nivel de Estrés y Calorías Quemadas:", correlacion_estres_cq)

# Segmentación por niveles de estrés (Alto: 7-10, Bajo: 1-4)
segmento_estres_alto = archivo.filter(pl.col("NE").is_between(7, 10))
segmento_estres_bajo = archivo.filter(pl.col("NE").is_between(1, 4))

# Cálculos de Promedio y Mediana para cada segmento en variables físicas
promedios_alto = segmento_estres_alto.select([
    pl.col("FCP").mean().alias("Promedio FCP"),
    pl.col("CQ").mean().alias("Promedio Calorías Quemadas"),
    pl.col("PS").mean().alias("Promedio Pasos Diarios")
])

medianas_alto = segmento_estres_alto.select([
    pl.col("FCP").median().alias("Mediana FCP"),
    pl.col("CQ").median().alias("Mediana Calorías Quemadas"),
    pl.col("PS").median().alias("Mediana Pasos Diarios")
])

promedios_bajo = segmento_estres_bajo.select([
    pl.col("FCP").mean().alias("Promedio FCP"),
    pl.col("CQ").mean().alias("Promedio Calorías Quemadas"),
    pl.col("PS").mean().alias("Promedio Pasos Diarios")
])

medianas_bajo = segmento_estres_bajo.select([
    pl.col("FCP").median().alias("Mediana FCP"),
    pl.col("CQ").median().alias("Mediana Calorías Quemadas"),
    pl.col("PS").median().alias("Mediana Pasos Diarios")
])

print("Promedios para Niveles de Estrés Alto:\n", promedios_alto)
print("Medianas para Niveles de Estrés Alto:\n", medianas_alto)
print("Promedios para Niveles de Estrés Bajo:\n", promedios_bajo)
print("Medianas para Niveles de Estrés Bajo:\n", medianas_bajo)

# Crear gráficos de los promedios para segmentos de estrés

def crear_grafico_segmento(data_alto, data_bajo, titulo, y_title, metrica, width=1200, height=800):
    chart = pygal.Bar(width=width, height=height)
    chart.title = titulo
    chart.x_title = "Segmento de Estrés"
    chart.y_title = y_title

    chart.add("Estrés Alto", data_alto[metrica][0])
    chart.add("Estrés Bajo", data_bajo[metrica][0])

    return chart

# Gráficos para Frecuencia Cardíaca Promedio
crear_grafico_segmento(promedios_alto, promedios_bajo, "Promedio de Frecuencia Cardíaca Promedio según Nivel de Estrés", "Frecuencia Cardíaca Promedio", "Promedio FCP").render_to_file("promedio_fcp_segmento.svg")

# Gráficos para Calorías Quemadas
crear_grafico_segmento(promedios_alto, promedios_bajo, "Promedio de Calorías Quemadas según Nivel de Estrés", "Calorías Quemadas", "Promedio Calorías Quemadas").render_to_file("promedio_calorias_segmento.svg")

# Gráficos para Pasos Diarios
crear_grafico_segmento(promedios_alto, promedios_bajo, "Promedio de Pasos Diarios según Nivel de Estrés", "Pasos Diarios", "Promedio Pasos Diarios").render_to_file("promedio_pasos_segmento.svg")
