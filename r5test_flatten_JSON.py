# importar las librerias requeridas (pandas, json)
import pandas as pd
import json

# definir la ruta de acceso al archivo json y el nombre del csv a crear
json_file = "taylor_swift_spotify.json"
csv_filename = "data.csv"

# cargar los datos del JSON
with open(json_file) as f:
    data = json.load(f)

# transformar el JSON en dataframe

main_df = pd.DataFrame(data)

# normalizar la infomracion contenida en la clave "albums"
df = pd.json_normalize(data, 'albums')

# expandir las columnas que contienen listas de diccionarios en filas separadas
# para cada item de la lista generando una estructura consistente
df = df.apply(lambda x: x.explode()).reset_index(drop=True)

# identificar las columnas que contienen diccionarios anidados para la
# normalizacion posterior
cols_to_normalize = ["tracks"]

# inicializar la lista vacia para almacenar el dataframe normalizado
normalized = list()
# iterar dentro de la lista "cocols_to_normalize"
# para normalizar los diccionarios anidados dentro de cada columna
# para este caso directamente "tracks" y añadirlos a la lista.
for col in cols_to_normalize:

    d = pd.json_normalize(df[col], sep='.')
    normalized.append(d.copy())

# combinar el dataframe original con los normalizados
# removiendo las columnas anidadas originales
df = pd.concat([df] + normalized, axis=1).drop(columns=cols_to_normalize)

# añadir la informacion del artista, comun a todas las filas.
df["artist_id"] = main_df["artist_id"][0]
df["artist_name"] = main_df["artist_name"][0]
df["artist_popularity"] = main_df["artist_popularity"][0]

# establecer el orden de las columnas para que coincida con el orden deseado
# para el CSV
cols = ["disc_number",
        "duration_ms",
        "explicit",
        "track_number",
        "track_popularity",
        "track_id",
        "track_name",
        "audio_features.danceability",
        "audio_features.energy",
        "audio_features.key",
        "audio_features.loudness",
        "audio_features.mode",
        "audio_features.speechiness",
        "audio_features.acousticness",
        "audio_features.instrumentalness",
        "audio_features.liveness",
        "audio_features.valence",
        "audio_features.tempo",
        "audio_features.id",
        "audio_features.time_signature",
        "artist_id",
        "artist_name",
        "artist_popularity",
        "album_id",
        "album_name",
        "album_release_date",
        "album_total_tracks"]

# ordenar el dataframe usando las columnas establecidas
ordered_df = df[cols]

# escribir el archivo CSV
ordered_df.to_csv(csv_filename, index=False)
