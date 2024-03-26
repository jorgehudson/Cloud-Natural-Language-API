# Instalar librerías
# pip install google-cloud-language
# pip install googletrans
# pip install pandas
# pip install bs4

from tabnanny import verbose
from google.cloud import language_v1
from google.cloud.language_v1 import Entity, EntityMention
from google.cloud.language_v1 import types
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

# Inicializar traductor
translator = Translator()

client = language_v1.LanguageServiceClient.from_service_account_json(filename="./tu_archivo.json") # Aquí la ruta completa del archivo con vuestra Clave API

# Introducir URL y Scraping de contenido
url = input("Introduce una URL para extraer su contenido: ")
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
text = str(soup.get_text().strip())

document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

# Entidades con su información
entities = client.analyze_entities(request={'document':document}).entities

# Crear listas para almacenar los datos
entidades_list = []
tipo_entidad_list = []
wiki_url_list = []
url_con_mid_list = []
prominencia_list = []

# Recorrer las entidades y agregar los datos a las listas
for entidad in entities:
    entidades_list.append(entidad.name)
    tipo_entidad_list.append(language_v1.Entity.Type(entidad.type_).name)
    wiki_url_list.append(entidad.metadata.get('wikipedia_url', 'Sin datos'))
    url_con_mid_list.append(f"https://www.google.com/search?q={entidad.name}&kponly&kgmid={entidad.metadata.get('mid', 'No existe id')}")
    prominencia_list.append(entidad.salience)

# Crear un DataFrame de pandas con los datos
data = {
    'Entidad': entidades_list,
    'Tipo Entidad': tipo_entidad_list,
    'Wiki URL': wiki_url_list,
    'URL con MID': url_con_mid_list,
    'Prominencia en el texto': prominencia_list
}

df = pd.DataFrame(data)

# Imprimir el DataFrame
print(df)

# Guardar el DataFrame como un archivo CSV
csv_filename = "entidades_analizadas.csv"
df.to_csv(csv_filename, index=False)
print(f"Se ha guardado el archivo CSV como '{csv_filename}'.")