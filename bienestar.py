import polars as pl
import pygal as py
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report


#cargo CSV a tratar 
datos = pl.read_csv('dataset-salud.csv')

#cambio los nombres de la columnas

datos = datos.rename({
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

#datos relevantes
columnas_relevantes = ["NE", "FCP", "HS", "CS", "PS", "CQ", "EA"]

#datos seleccionados segun lo relevante
datos = datos.select(columnas_relevantes)

#eliminar null
datos = datos.drop_nulls()


#extraer estado de animo
estado_animo = datos['EA'].to_numpy()

#Convertir los calores categoricos en numericos
le = LabelEncoder()

#codificamos estado de animo
estado_animo_codificado = le.fit_transform(estado_animo)


datos = datos.with_columns(pl.Series("EA_codificado", estado_animo_codificado))

print(datos)



# Seleccionar las columnas numéricas a normalizar
variables_a_normalizar = ["NE", "FCP", "HS", "CS", "PS", "CQ"]

# Crear un scaler y ajustar los datos
scaler = MinMaxScaler()
datos_normalizados = scaler.fit_transform(datos.select(variables_a_normalizar).to_numpy())

# Convertir los datos normalizados a un DataFrame Polars
datos_normalizados = pl.DataFrame(datos_normalizados, schema=variables_a_normalizar)

# Añadir la columna codificada de estado de ánimo al DataFrame normalizado
datos_normalizados = datos_normalizados.with_columns(datos["EA_codificado"])

print(datos_normalizados)


# Separar las características (X) y la variable objetivo (y)
X = datos_normalizados.select(["NE", "FCP", "HS", "CS", "PS", "CQ"]).to_numpy()
y = datos_normalizados["EA_codificado"].to_numpy()

# Dividir en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Conjunto de entrenamiento:", X_train.shape)
print("Conjunto de prueba:", X_test.shape)



# Crear y entrenar el modelo k-NN
modelo_knn = KNeighborsClassifier(n_neighbors=3)  # k=3
modelo_knn.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba
predicciones = modelo_knn.predict(X_test)

print("Predicciones:", predicciones)

# Calcular la precisión
precision = accuracy_score(y_test, predicciones)
print("Precisión del modelo:", precision)

# Reporte detallado de las métricas
reporte = classification_report(y_test, predicciones, target_names=le.classes_)
print(reporte)



grafico = py.Bar()
grafico.title = "Distribución de Predicciones"
categorias = le.classes_

# Contar las predicciones por categoría
conteo_predicciones = pl.DataFrame(predicciones, schema=["Predicciones"]).group_by("Predicciones").count()

# Agregar datos al gráfico
for categoria, conteo in zip(categorias, conteo_predicciones["count"]):
    grafico.add(categoria, conteo)

# Guardar el gráfico como archivo SVG
grafico.render_to_file("predicciones.svg")
print("Gráfico generado: predicciones.svg")

