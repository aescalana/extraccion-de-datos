import json

import requests

# Reducir nivel de seguridad para permitir la comunicación con el servidor
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

ENDPOINT_URL = 'https://cedulaprofesional.sep.gob.mx/cedula/buscaCedulaJson.action'
# Crear los datos, tal y como se usan en la página
data = {}
data['json'] = json.dumps(
    dict(
        maxResult='1000',
        nombre='ANA LIDIA',
        paterno='FRANZONI',
        materno='VELAZQUEZ',
        idCedula='',
    )
)

# Enviar la petición
response = requests.post(ENDPOINT_URL, data=data)

# Procesar la respuesta
response_json = response.json()
for item in response_json['items']:
    print(item['idCedula'])
