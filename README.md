# Data-Quality-Engineer-Prueba-Tecnica---R5
Repositorio de entregables de prueba tecnica para aspirar al cargo de  Data Quality Engineer en R5

Contiene los siguientes archivos

## Take Home Project - Data Quality Engineer.pdf
    pdf con los requerimientos presentados en la prueba tecnica.
## taylor_swift_spotify.json
    JSON con la informacion de taylor swift obtenida a traves de la API de spotify

## r5test_flatten_JSON.py

codigo de python con la siguiente estructura y proposito:

### 1. Importando librerías:

import pandas as pd: Importa la librería Pandas para manipular y analizar datos.
import json: Importa la librería JSON para trabajar con datos en formato JSON.

### 2. Especificando archivos:

json_file = "/content/taylor_swift_spotify.json": Asigna la ruta al archivo JSON que contiene los datos de Spotify de Taylor Swift.
csv_filename = "data.csv": Asigna el nombre deseado para el archivo CSV de salida.
### 3. Cargando datos JSON:

with open(json_file) as f:: Abre el archivo JSON en modo de lectura.
data = json.load(f): Carga los datos JSON en un diccionario de Python.
### 4. Normalizando los datos:

main_df = pd.json_normalize(data): Crea un DataFrame a partir de todo el JSON, aplanando estructuras anidadas.
df = pd.json_normalize(data, 'albums'): Crea un DataFrame específicamente para la clave "albums" en el JSON, enfocándose en la información relacionada a los álbumes.
df = df.apply(lambda x: x.explode()).reset_index(drop=True): Expande cualquier columna que contenga listas de diccionarios en filas separadas para cada elemento de la lista, asegurando una estructura consistente.
### 5. Normalizando datos anidados:

cols_to_normalize = ["tracks"]: Identifica las columnas que contienen diccionarios anidados que necesitan normalización adicional.
normalized = list(): Inicializa una lista vacía para almacenar los DataFrames normalizados.
for col in cols_to_normalize:: Itera a través de las columnas para normalizar.
d = pd.json_normalize(df[col], sep='.'): Normaliza los diccionarios anidados dentro de la columna especificada.
d.columns = [f'{col}.{v}' for v in d.columns]: Agrega el nombre de la columna como prefijo para evitar posibles conflictos de nombres de columna.
normalized.append(d.copy()): Agrega el DataFrame normalizado a la lista.
df = pd.concat([df] + normalized, axis=1).drop(columns=cols_to_normalize): Combina el DataFrame original con los DataFrames normalizados, eliminando las columnas anidadas originales.
### 6. Añadiendo información del artista:

df["artist_id"] = main_df["artist_id"][0]: Agrega el ID del artista desde el DataFrame principal al DataFrame de álbumes.
df["artist_name"] = main_df["artist_name"][0]: Agrega el nombre del artista desde el DataFrame principal al DataFrame de álbumes.
df["artist_popularity"] = main_df["artist_popularity"][0]: Agrega la popularidad del artista desde el DataFrame principal al DataFrame de álbumes.
### 7. Ordenando columnas:

cols = [...]: Especifica el orden deseado de las columnas en el DataFrame final.
ordered_df = df[cols]: Reordena las columnas en el orden especificado.
### 8. Escribiendo archivo CSV:

ordered_df.to_csv(csv_filename, index=False): Escribe el DataFrame a un archivo CSV con el nombre especificado, excluyendo el índice.

###En resumen, este código:

Carga y estructura los datos de Spotify para los álbumes de Taylor Swift desde un archivo JSON.
Aplana los datos anidados para facilitar el análisis en formato tabular.
Combina información de diferentes niveles de la estructura JSON.
Organiza los datos para mayor claridad y consistencia.
Crea un archivo CSV bien formateado para un análisis posterior.
