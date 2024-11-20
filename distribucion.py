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

# Crear una columna 'RangoEdad' para agrupar por intervalos de edad
archivo = archivo.with_columns(
    pl.when(pl.col("ED") < 25).then(pl.lit("18-25"))
    .when(pl.col("ED") < 35).then(pl.lit("26-35"))
    .when(pl.col("ED") < 45).then(pl.lit("36-45"))
    .otherwise(pl.lit("45+")).alias("RangoEdad")
)

# Calcular la mediana, percentiles y promedios para cada hábito por grupo de edad y género
analisis_habitos = archivo.group_by(["SX", "RangoEdad"]).agg([
    pl.col("PS").median().alias("Mediana Pasos"),
    pl.col("PS").quantile(0.25).alias("Percentil 25 Pasos"),
    pl.col("PS").quantile(0.75).alias("Percentil 75 Pasos"),
    pl.col("PS").mean().alias("Promedio Pasos"),
    
    pl.col("CQ").median().alias("Mediana Calorías Quemadas"),
    pl.col("CQ").quantile(0.25).alias("Percentil 25 Calorías Quemadas"),
    pl.col("CQ").quantile(0.75).alias("Percentil 75 Calorías Quemadas"),
    pl.col("CQ").mean().alias("Promedio Calorías Quemadas"),
    
    pl.col("HS").median().alias("Mediana Horas de Sueño"),
    pl.col("HS").quantile(0.25).alias("Percentil 25 Horas de Sueño"),
    pl.col("HS").quantile(0.75).alias("Percentil 75 Horas de Sueño"),
    pl.col("HS").mean().alias("Promedio Horas de Sueño")
])

# Función para crear gráficos con Pygal
def crear_grafico_metrica(data, titulo, y_title, metrica, width=1200, height=800):
    chart = pygal.Bar(width=width, height=height)
    chart.title = titulo
    chart.x_title = "Rango de Edad y Sexo"
    chart.y_title = y_title

    for row in data.iter_rows(named=True):
        label = f"{row['RangoEdad']} ({row['SX']})"
        chart.add(label, row[metrica])

    return chart

# Gráficos de promedios
crear_grafico_metrica(analisis_habitos, "Promedio de Pasos Diarios por Rango de Edad y Sexo", "Promedio de Pasos Diarios", "Promedio Pasos").render_to_file("promedio_pasos.svg")
crear_grafico_metrica(analisis_habitos, "Promedio de Calorías Quemadas por Rango de Edad y Sexo", "Promedio de Calorías Quemadas", "Promedio Calorías Quemadas").render_to_file("promedio_calorias.svg")
crear_grafico_metrica(analisis_habitos, "Promedio de Horas de Sueño por Rango de Edad y Sexo", "Promedio de Horas de Sueño", "Promedio Horas de Sueño").render_to_file("promedio_horas_sueno.svg")

# Gráficos de mediana
crear_grafico_metrica(analisis_habitos, "Mediana de Pasos Diarios por Rango de Edad y Sexo", "Mediana de Pasos Diarios", "Mediana Pasos").render_to_file("mediana_pasos.svg")
crear_grafico_metrica(analisis_habitos, "Mediana de Calorías Quemadas por Rango de Edad y Sexo", "Mediana de Calorías Quemadas", "Mediana Calorías Quemadas").render_to_file("mediana_calorias.svg")
crear_grafico_metrica(analisis_habitos, "Mediana de Horas de Sueño por Rango de Edad y Sexo", "Mediana de Horas de Sueño", "Mediana Horas de Sueño").render_to_file("mediana_horas_sueno.svg")

# Gráficos de percentiles 25
crear_grafico_metrica(analisis_habitos, "Percentil 25 de Pasos Diarios por Rango de Edad y Sexo", "Percentil 25 de Pasos Diarios", "Percentil 25 Pasos").render_to_file("percentil_25_pasos.svg")
crear_grafico_metrica(analisis_habitos, "Percentil 25 de Calorías Quemadas por Rango de Edad y Sexo", "Percentil 25 de Calorías Quemadas", "Percentil 25 Calorías Quemadas").render_to_file("percentil_25_calorias.svg")
crear_grafico_metrica(analisis_habitos, "Percentil 25 de Horas de Sueño por Rango de Edad y Sexo", "Percentil 25 de Horas de Sueño", "Percentil 25 Horas de Sueño").render_to_file("percentil_25_horas_sueno.svg")

# Gráficos de percentiles 75
crear_grafico_metrica(analisis_habitos, "Percentil 75 de Pasos Diarios por Rango de Edad y Sexo", "Percentil 75 de Pasos Diarios", "Percentil 75 Pasos").render_to_file("percentil_75_pasos.svg")
crear_grafico_metrica(analisis_habitos, "Percentil 75 de Calorías Quemadas por Rango de Edad y Sexo", "Percentil 75 de Calorías Quemadas", "Percentil 75 Calorías Quemadas").render_to_file("percentil_75_calorias.svg")
crear_grafico_metrica(analisis_habitos, "Percentil 75 de Horas de Sueño por Rango de Edad y Sexo", "Percentil 75 de Horas de Sueño", "Percentil 75 Horas de Sueño").render_to_file("percentil_75_horas_sueno.svg")
