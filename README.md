# AnimeWallpaperManager

Este script en Python descarga imágenes de anime aleatorias desde la API de waifu.pics, mejora la calidad aplicando desenfoque a imágenes verticales, y las configura automáticamente como fondo de pantalla en Windows. Además, guarda las imágenes originales sin modificar para uso posterior.

## Cómo usar:

### Instala las dependencias:
1. Asegúrate de tener Python instalado.
2. Ejecuta el siguiente comando para instalar las bibliotecas necesarias:
   ```bash
   pip install requests pillow

 
#### Ejecuta el script:
1. Cada vez que inicies sesión en tu PC, ejecuta el script para que descargue y configure un nuevo fondo de pantalla:
python wallpaper_manager.py
2. El script descargará una nueva imagen cada 5 minutos y la aplicará automáticamente como fondo de pantalla.
3.Notas:
Guardar las imágenes: Las imágenes originales se guardarán en la carpeta originales, dentro del directorio especificado en el script.
Inicio automático: Para que el script se ejecute automáticamente al iniciar sesión, puedes agregar un acceso directo al archivo .py en la carpeta de inicio de Windows.
