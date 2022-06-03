import json
import os.path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

ALUMNI_PATH = r'C:\Users\Alejandro\Downloads\alumni.json'
DRIVER_PATH = r'C:\Users\Alejandro\Downloads\chromedriver.exe'
PAGE_URL = 'http://escolar1.rhon.itam.mx/titulacion/programas.asp'
ANCHOR_CSS_SELECTOR = 'td:first-child table a'
NAME_CSS_SELECTOR = 'table[border="1"] tr:not(:first-child) td:first-child'
YEAR_CSS_SELECTOR = 'table[border="1"] tr:not(:first-child) td:not(:first-child)'

if os.path.exists(ALUMNI_PATH):
    # Cargar el resultado anterior
    with open(ALUMNI_PATH) as alumni_file:
        alumni = json.load(alumni_file)
else:
    # Inicia el navegador de manera visual
    driver = webdriver.Chrome(service=Service(DRIVER_PATH))

    # Carga la página y selecciona los vínculos
    driver.get(PAGE_URL)
    anchor_elements = driver.find_elements(by=By.CSS_SELECTOR, value=ANCHOR_CSS_SELECTOR)

    # Procesar vínculos antes de cambiar de página
    anchor_list = [(anchor.text, anchor.get_attribute("href")) for anchor in anchor_elements]

    alumni = {}
    # Para cada vínculo:
    for degree, url in anchor_list:
        # 1. Cargar la página
        driver.get(url)
        # 2. Seleccionar los nombres y los años
        name_list = driver.find_elements(by=By.CSS_SELECTOR, value=NAME_CSS_SELECTOR)
        year_list = driver.find_elements(by=By.CSS_SELECTOR, value=YEAR_CSS_SELECTOR)
        # 3. Comenzar o extender la lista de títulos de cada exalumno
        for index in range(len(name_list)):
            student_name = name_list[index].text
            year = year_list[index].text
            if student_name in alumni:
                alumni[student_name].append((degree, year))
            else:
                alumni[student_name] = [(degree, year)]

    # Guardar el resultado
    with open(ALUMNI_PATH, 'w') as alumni_file:
        json.dump(alumni, alumni_file)

    # Cierra el navegador
    driver.quit()

# Imprime alumnos con más de un título
for name, degrees in alumni.items():
    if len(degrees) > 1:
        print(f'{name} has {len(degrees)} degrees: {degrees}')
