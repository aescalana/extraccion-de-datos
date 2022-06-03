import json
import os.path
import time

import requests

from auxiliary_functions import analyze_api_results
from auxiliary_functions import analyze_scraper_results
from auxiliary_functions import filter_alumni
from auxiliary_functions import restructure_alumni

# Reducir nivel de seguridad para permitir la comunicación con el servidor
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

QPS = 20
ALUMNI_PATH = r'C:\Users\Alejandro\Downloads\alumni.json'
ALUMNI_API_PATH = r'C:\Users\Alejandro\Downloads\alumni_api.json'
ENDPOINT_URL = 'https://cedulaprofesional.sep.gob.mx/cedula/buscaCedulaJson.action'
ITAM_OFFICIAL_NAME = 'INSTITUTO TECNOLÓGICO AUTÓNOMO DE MÉXICO'

# Cargar los resultados del scraper
with open(ALUMNI_PATH) as alumni_file:
    alumni = json.load(alumni_file)

# Imprimir análisis de los resultados del scraper
analyze_scraper_results(alumni)

# Filtrar a los alumnos y títulos que cumplan con 2 reglas:
# 1. El nombre completo del alumno está conformado por exactamente 3 palabras
# 2. El nombre del título coincide con los registros de la SEP
filtered_alumni = filter_alumni(alumni)

# Cargar el resultado anterior de este guión, si ya existe
if os.path.exists(ALUMNI_API_PATH):
    with open(ALUMNI_API_PATH) as alumni_api_file:
        restructured_alumni = json.load(alumni_api_file)
else:
    # Cambiar la estructura de los datos para un manejo más simple
    restructured_alumni = restructure_alumni(filtered_alumni)

    start_seconds = time.time()
    for name, info in restructured_alumni.items():
        # Obtener resultados de la API
        info['api_output'] = requests.post(ENDPOINT_URL, data=info['api_input']).json()
        # Esperar una fracción de segundo para no saturar de peticiones la API
        time.sleep(1/QPS)
        for degree in info['degrees']:
            for item in info['api_output']['items']:
                if degree['title_name'] in item['titulo'] and item['desins'] == ITAM_OFFICIAL_NAME:
                    degree.update(item)
                    break

    # Imprimir el tiempo que tardó en ejecutar
    end_seconds = time.time()
    print(f'\n\nTotal segundos: {end_seconds - start_seconds:.2f}')

    # Guardar los resultados
    with open(ALUMNI_API_PATH, 'w') as alumni_api_file:
        json.dump(restructured_alumni, alumni_api_file)

# Procesar la respuesta
analyze_api_results(restructured_alumni)
