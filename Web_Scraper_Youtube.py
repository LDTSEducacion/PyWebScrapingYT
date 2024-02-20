from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pyautogui
import csv

# Tiempo de inicio
tiempo_inicio = time.time()

# URLs a las que haremos scraping, tienen que terminar por /videos
# Tener en cuenta que mientras mas urls mas tiempo tardara el programa
urls = [
    "https://www.youtube.com/@HiClavero/videos",
    "https://www.youtube.com/@ldtssoftware8782/videos",
    "https://www.youtube.com/@LDTSAcademy/videos"
] 

# Lista donde guardaremos los datos de los canales
datosCanales = [
    ['UrlUsuario', 'NumSubscriptores', 'NumVideos', 'Descripcion']
]

# Lista donde guardaremos los datos de los videos
datosVideos = [
    ['UrlUsuario', 'TituloVideo', 'NumVisualizaciones', 'DiaSubida']
]

# Recorremos la lista de URLs
for url in urls:
    driver = webdriver.Chrome()
    driver.get(url)

    # Esperamos 5 segundos a que la pagina se cargue
    time.sleep(5)

    # Movemos el ratón a una posición específica para poder aceptar las cookies
    pyautogui.moveTo(x=850, y=920, duration=1)

    # Hacemos click
    pyautogui.click()

    # Esperamos otros 5 segundos para que la pagina se cargue
    # Obtenemos el contenido de la pagina
    content = driver.page_source.encode('utf-8').strip()

    # Convertimos el contenido a BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Obtenemos los subscriptores del canal
    subscriptores = soup.find('yt-formatted-string', id='subscriber-count').text.strip().split(' ')[0]

    # Obtenemos el numero de videos del canal
    numVideos = soup.find('yt-formatted-string', id='videos-count').text.strip().split(' ')[0]

    # Obtenemos la descripcion del canal
    descripcion = soup.find('div', attrs={'id': 'content', 'class': 'style-scope ytd-channel-tagline-renderer'}).text.strip()

    # Guardamos en la lista datosCanales los subscriptores, numVideos y descripcion
    datosCanales.append([url.split('/videos')[0], subscriptores, numVideos, descripcion])

    # Obtenemos los titulos de todos los videos
    titulosVideos =soup.findAll('yt-formatted-string', id='video-title')

    # Obtenemos el numero de visualizaciones y el numero de dias de todos los videos
    viewsAndDaysVideos = soup.findAll('span', class_='inline-metadata-item style-scope ytd-video-meta-block')

    # Separamos las visualizaciones de las fechas de subidas, para ello:
    visualizaciones = []
    subidaDias = []

    # Primero las visualizaciones
    for i in range(0, len(viewsAndDaysVideos), 2):
        visualizaciones.append(viewsAndDaysVideos[i])
    
    # Ahora los dias de subida
    for i in range(1, len(viewsAndDaysVideos), 2):
        subidaDias.append(viewsAndDaysVideos[i])

    # Ahora guardamos los 10 primeros videos del canal
    for i in range(0, 10):
        # Añadimos a la lista datosVideos
        datosVideos.append([url.split('/videos')[0], titulosVideos[i].text, visualizaciones[i].text, subidaDias[i].text])

    # Cerramos el navegador
    driver.quit()

# Escribimos los datos de los videos en un fichero CSV
with open('videos.csv', 'w', encoding='utf-8', newline='') as fichero:
    escritor_csv = csv.writer(fichero, delimiter=';')
    # Escribimos los datos en el fichero csv
    escritor_csv.writerows(datosVideos)

# Escribimos los datos de los canales en un fichero CSV
with open('canales.csv', 'w', encoding='utf-8', newline='') as fichero:
    escritor_csv = csv.writer(fichero, delimiter=';')
    # Escribimos los datos en el fichero csv
    escritor_csv.writerows(datosCanales)


# Tiempo de fin
tiempo_fin = time.time()

# Calcula tiempo
tiempo_total = tiempo_fin - tiempo_inicio

# Mostramos por consola el tiempo total
print(f"El código ha tardado {tiempo_total}s")