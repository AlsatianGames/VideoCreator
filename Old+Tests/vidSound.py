from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
import pyttsx3
import pandas as pd
import os
from PIL import Image  # Asegúrate de importar esto
import PIL.Image

# Inicializar pyttsx3
engine = pyttsx3.init()

# Leer el archivo CSV
def leer_csv(archivo_csv):
    return pd.read_csv(archivo_csv)

# Función para generar el audio de la frase usando pyttsx3 y guardarlo como un archivo .mp3
def generar_audio(frase, ruta_audio):
    engine.save_to_file(frase, ruta_audio)
    engine.runAndWait()
    return ruta_audio

# Función para crear un video con letras animadas y con sonido
def generar_videos(df):
    for index, row in df.iterrows():
        frase = row['frase']
        tiempo = float(row['tiempo'])

        # Crear la carpeta para cada frase
        nombre_carpeta = f"frases"
        if not os.path.exists(nombre_carpeta):
            os.makedirs(nombre_carpeta)

        # Ruta de los archivos dentro de la carpeta
        nombre_archivo_audio = os.path.join(nombre_carpeta, f"audio_frase_{index+1}.mp3")
        nombre_archivo_video = os.path.join(nombre_carpeta, f"video_frase_{index+1}.mp4")

        # Generar el archivo de audio
        generar_audio(frase, nombre_archivo_audio)

        # Crear un TextClip con animación de fadein y fuente Impact
        texto_clip = (TextClip(frase, fontsize=160, color='white', size=(1080, 1920), font='Impact', method='caption', bg_color='black')
                      .set_duration(tiempo)
                      .fadein(1))  # Aplicar el efecto de fade in durante 1 segundo

        # Aplicar un zoom in progresivo durante el tiempo del texto
        texto_clip = texto_clip.resize(lambda t: 1 + 0.02 * t)

        # Añadir el audio al video
        audio_clip = AudioFileClip(nombre_archivo_audio)
        video_con_audio = texto_clip.set_audio(audio_clip)

        # Exportar el video en formato MP4 dentro de la carpeta
        video_con_audio.write_videofile(nombre_archivo_video, fps=24)
        print(f"Video generado: {nombre_archivo_video}")

# Función principal
def main():
    archivo_csv = "C:\\Users\\Taliex4\\Documents\\Codigo\\frases.csv"  # Nombre del archivo CSV con las frases y tiempos
    df = leer_csv(archivo_csv)
    generar_videos(df)

if __name__ == "__main__":
    main()
