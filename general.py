import polars as pl
import pygal as py


# Cargar el archivo CSV
datos = pl.read_csv('dataset-salud.csv')

datos = datos.rename({
    'Fecha': 'Date',
    'Sexo': 'SX',  # Aquí asegúrate de que el CSV tiene una columna llamada 'Sexo'
    'Edad': 'ED',
    'Pasos diarios': 'PS',
    'Calorías quemadas': 'CQ',
    'Horas de sueño': 'HS',
    'Calidad del sueño': 'CS',
    'Frecuencia cardíaca promedio': 'FCP',
    'Nivel de estrés': 'NE',
    'Estado de ánimo': 'EA'
})


# Agrupar y contar el número de hombres y mujeres
conteo_sexo = datos.group_by("SX").count()
print(conteo_sexo)



# Crear gráfico de pastel con Pygal
grafico_pastel = py.Pie()
grafico_pastel.title = "Distribución de Hombres y Mujeres Atendidos"

# Agregar datos al gráfico
for sexo, cantidad in zip(conteo_sexo["SX"], conteo_sexo["count"]):
    grafico_pastel.add(sexo, cantidad)

# Guardar como SVG
grafico_pastel.render_to_file("hombres_mujeres_pastel.svg")
print("Gráfico generado: hombres_mujeres_pastel.svg")
