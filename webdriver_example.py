import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = r'C:\Users\Alejandro\Downloads\chromedriver.exe'
PAGE_URL = 'https://www.itam.mx'

# Inicia el navegador de manera visual
driver = webdriver.Chrome(service=Service(DRIVER_PATH))

# Carga la página e imprime el título de la página
driver.get(PAGE_URL)
print(driver.title)

# Espera 3 segundos y cierra el navegador
time.sleep(3)
driver.quit()
