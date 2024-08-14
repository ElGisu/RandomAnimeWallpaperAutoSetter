import requests
from PIL import Image, ImageFilter
from io import BytesIO
import ctypes
import os
import hashlib
import time

def download_and_set_wallpaper():
    # Directorio donde se guardarán las imágenes
    save_directory = r"C:\Users\jcevi\OneDrive\Desktop\Nueva carpeta (2)"
    original_images_directory = os.path.join(save_directory, "originales")
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    if not os.path.exists(original_images_directory):
        os.makedirs(original_images_directory)

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

    # Genera un hash para verificar si la imagen ya existe
    img_hash = hashlib.md5(img.tobytes()).hexdigest()
    existing_images = [f for f in os.listdir(save_directory) if f.endswith('.png')]
    existing_hashes = {os.path.splitext(f)[0]: f for f in existing_images}

    # Verifica si la imagen ya fue guardada anteriormente
    if img_hash not in existing_hashes:
        # Guardar la imagen original sin el efecto de desenfoque
        original_image_path = os.path.join(original_images_directory, f'{img_hash}.png')
        img.save(original_image_path)
        print(f"Imagen original guardada en: {original_image_path}")

        # Obtén la resolución de la pantalla
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)

        # Crear una copia de la imagen desenfocada para usar como fondo completo
        img_blurred = img.copy()

        # Redimensionar la imagen desenfocada para llenar la pantalla
        img_blurred = img_blurred.resize((screen_width, screen_height), Image.LANCZOS)
        img_blurred = img_blurred.filter(ImageFilter.GaussianBlur(radius=20))

        # Redimensiona la imagen original manteniendo la proporción
        img.thumbnail((screen_width, screen_height), Image.LANCZOS)

        # Pegar la imagen original sobre la versión desenfocada, centrada
        offset = ((screen_width - img.width) // 2, (screen_height - img.height) // 2)
        img_blurred.paste(img, offset)

        # Guarda la imagen final con el desenfoque aplicado
        final_image_path = os.path.join(save_directory, f'{img_hash}.png')
        img_blurred.save(final_image_path)

        # Configura la imagen combinada como fondo de pantalla
        ctypes.windll.user32.SystemParametersInfoW(20, 0, final_image_path, 0)
        print("Imagen con fondo desenfocado configurada como fondo de pantalla.")

        # Elimina las imágenes más antiguas si se supera el límite de 50
        if len(existing_images) >= 50:
            oldest_image = min(existing_images, key=lambda x: os.path.getctime(os.path.join(save_directory, x)))
            os.remove(os.path.join(save_directory, oldest_image))
            print(f"Eliminada imagen antigua: {oldest_image}")
    else:
        print("La imagen ya existe y no se guardará nuevamente.")
        return

while True:
    download_and_set_wallpaper()
    # Espera 5 minutos (300 segundos)
    time.sleep(300)
