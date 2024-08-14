mport requests
from PIL import Image, ImageFilter
from io import BytesIO
import ctypes
import os
import hashlib
import time

def download_and_set_wallpaper():
    # Directorio donde se guardarán las imágenes originales
    save_directory = r"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Archivo para almacenar los hashes de las imágenes ya descargadas
    hash_file_path = os.path.join(save_directory, "image_hashes.txt")
    
    # Cargar los hashes existentes
    if os.path.exists(hash_file_path):
        with open(hash_file_path, 'r') as f:
            downloaded_hashes = set(f.read().splitlines())
    else:
        downloaded_hashes = set()

    while True:
        # URL de la API que devuelve una imagen de anime aleatoria
        url = "https://api.waifu.pics/sfw/waifu"

        # Realiza la solicitud a la API
        response = requests.get(url)
        data = response.json()

        # Obtiene la URL de la imagen
        image_url = data['url']

        # Descarga la imagen
        image_response = requests.get(image_url)
        img = Image.open(BytesIO(image_response.content))

        # Genera un hash para el nombre del archivo
        img_hash = hashlib.md5(img.tobytes()).hexdigest()

        # Si la imagen ya ha sido descargada, omitirla y continuar
        if img_hash in downloaded_hashes:
            print("Imagen repetida, descargando otra...")
            continue

        # Agregar el hash al conjunto de hashes descargados
        downloaded_hashes.add(img_hash)
        with open(hash_file_path, 'a') as f:
            f.write(f"{img_hash}\n")

        # Guarda la imagen original
        original_image_path = os.path.join(save_directory, f'{img_hash}.png')
        img.save(original_image_path)

        # Verifica la relación de aspecto para determinar si aplicar desenfoque
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        img_aspect_ratio = img.width / img.height
        screen_aspect_ratio = screen_width / screen_height

        if img_aspect_ratio <= screen_aspect_ratio:
            # La imagen es vertical o cercana a la proporción de la pantalla, aplica desenfoque
            img_blurred = img.copy()
            img_blurred = img_blurred.resize((screen_width, screen_height), Image.LANCZOS)
            img_blurred = img_blurred.filter(ImageFilter.GaussianBlur(radius=20))
            img.thumbnail((screen_width, screen_height), Image.LANCZOS)
            offset = ((screen_width - img.width) // 2, (screen_height - img.height) // 2)
            img_blurred.paste(img, offset)

            # Establece la imagen desenfocada como fondo de pantalla
            blurred_image_path = os.path.join(save_directory, f'{img_hash}_blurred.png')
            img_blurred.save(blurred_image_path)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, blurred_image_path, 0)
        else:
            # La imagen es horizontal o suficientemente amplia, se establece tal cual
            ctypes.windll.user32.SystemParametersInfoW(20, 0, original_image_path, 0)

        print("Imagen configurada como fondo de pantalla.")
        break

while True:
    download_and_set_wallpaper()
    # Espera 5 minutos (300 segundos)
    time.sleep(300)
