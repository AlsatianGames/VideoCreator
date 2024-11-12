
# Generador de Videos con Frases

Este proyecto es una aplicación que genera videos personalizados a partir de frases y tiempos definidos en un archivo CSV. Cada frase se convierte en un video independiente con texto animado y un audio generado automáticamente a partir de la frase.

## Características

- Convierte frases de un archivo CSV en clips de video con texto animado.
- Genera automáticamente el audio de cada frase utilizando `pyttsx3`.
- Exporta cada frase en un video independiente en formato MP4.
- Interfaz gráfica simple y funcional, construida en Tkinter.

## Requisitos Previos

Asegúrate de tener instaladas las siguientes bibliotecas de Python antes de ejecutar el proyecto:

- `moviepy`
- `pyttsx3`
- `pandas`
- `tkinter` (incluida en la mayoría de instalaciones de Python)
  
Para instalar las dependencias, puedes usar:
```bash
pip install moviepy pyttsx3 pandas
```

## Instrucciones de Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/AlsatianGames/VideoCreator.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd VideoCreator
    ```
3. Instala las dependencias mencionadas anteriormente.

## Uso

1. Ejecuta el script principal:
    ```bash
    python VideoCreator.py
    ```
2. Se abrirá una interfaz gráfica donde podrás seleccionar un archivo CSV.
3. El archivo CSV debe tener el siguiente formato:
   - `frase`: la frase a incluir en el video.
   - `tiempo`: la duración en segundos que el texto debe aparecer en el video.
   
### Ejemplo de archivo CSV

```csv
frase,tiempo
"Bienvenido al generador de videos",3
"Esto es una prueba de frase",4
```

4. Al seleccionar el archivo, se generarán videos para cada frase del archivo CSV y se guardarán en una carpeta llamada `frases`.

## Estructura del Proyecto

- `VideoCreator.py`: Script principal que incluye la lógica de la aplicación.
- `frases/`: Carpeta donde se guardan los videos generados para cada frase.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
