from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

DRIVER_PATH = r'C:\Users\Alejandro\Downloads\chromedriver.exe'
PAGE_URL = 'http://escolar1.rhon.itam.mx/titulacion/programas.asp'
ANCHOR_CSS_SELECTOR = 'td:first-child table a'

# Inicia el navegador de manera visual
driver = webdriver.Chrome(service=Service(DRIVER_PATH))

# Carga la página y selecciona los vínculos
driver.get(PAGE_URL)
anchor_list = driver.find_elements(by=By.CSS_SELECTOR, value=ANCHOR_CSS_SELECTOR)

# Para cada vínculo, imprimir el URL
for anchor in anchor_list:
    print(f'{anchor.text}: {anchor.get_attribute("href")}')

# Cierra el navegador
driver.quit()
