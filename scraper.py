from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

DRIVER_PATH = r'C:\Users\Alejandro\Downloads\chromedriver.exe'
PAGE_URL = 'http://escolar1.rhon.itam.mx/titulacion/titulados.asp?prog=000009'
NAME_CSS_SELECTOR = 'table[border="1"] tr:not(:first-child) td:first-child'
YEAR_CSS_SELECTOR = 'table[border="1"] tr:not(:first-child) td:not(:first-child)'

# Inicia el navegador de manera visual
driver = webdriver.Chrome(service=Service(DRIVER_PATH))

# Carga la página
driver.get(PAGE_URL)

# Seleccionar las celdas con el nombre
name_list = driver.find_elements(by=By.CSS_SELECTOR, value=NAME_CSS_SELECTOR)
# Seleccionar las celdas con el año
year_list = driver.find_elements(by=By.CSS_SELECTOR, value=YEAR_CSS_SELECTOR)

# Para cada par de celdas, imprimir el nombre y el año
for index in range(len(name_list)):
    print(f'{name_list[index].text}: {year_list[index].text}')

# Cierra el navegador
driver.quit()
