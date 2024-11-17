from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, VideoFileClip, concatenate_videoclips, concatenate_audioclips
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS  # Parche para compatibilidad con MoviePy

import pyttsx3
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Inicializar pyttsx3
engine = pyttsx3.init()

# Función para generar el audio de la frase usando pyttsx3 y guardarlo como un archivo .mp3
def generar_audio(frase, ruta_audio):
    engine.save_to_file(frase, ruta_audio)
    engine.runAndWait()
    return ruta_audio

# Función para ajustar la duración del audio para que coincida con el tiempo especificado
def ajustar_duracion_audio(nombre_archivo_audio, duracion_objetivo):
    audio_clip = AudioFileClip(nombre_archivo_audio)
    duracion_audio = audio_clip.duration

    if duracion_audio < duracion_objetivo:
        # Crear un clip de silencio para completar el tiempo restante
        silence_duration = duracion_objetivo - duracion_audio
        silence = AudioFileClip("C:/Users/Taliex4/Documents/Codigo/VideoCreator/silence.mp3").set_duration(silence_duration)
        audio_clip = concatenate_audioclips([audio_clip, silence])
    return audio_clip.set_duration(duracion_objetivo)

def generar_videos_individuales(df, video_fondo_path, progress_bar, root):
    clips = []
    total = len(df)
    progress_bar["maximum"] = total

    # Crear la carpeta para almacenar los videos de frases
    nombre_carpeta = "videos_frases"
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)

    # Cargar el video de fondo y ajustar la opacidad al 90%
    try:
        video_fondo = VideoFileClip(video_fondo_path).resize((1080, 1920)).set_opacity(0.1)
        print("Video de fondo cargado correctamente dentro de generar_videos_individuales.")
    except Exception as e:
        print("Error al cargar el video de fondo dentro de generar_videos_individuales:", e)
        return

    for index, row in df.iterrows():
        frase = row['frase']
        tiempo = float(row['tiempo'])

        # Rutas de los archivos de audio y video
        nombre_archivo_audio = os.path.join(nombre_carpeta, f"audio_frase_{index+1}.mp3")
        nombre_archivo_video = os.path.join(nombre_carpeta, f"video_frase_{index+1}.mp4")
        print(f"Generando archivo de audio: {nombre_archivo_audio}")
        print(f"Generando archivo de video: {nombre_archivo_video}")

        # Generar el archivo de audio para la frase
        generar_audio(frase, nombre_archivo_audio)

        # Asegurarse de que el archivo de audio se generó correctamente
        if not os.path.exists(nombre_archivo_audio):
            print(f"Error: No se generó el archivo de audio: {nombre_archivo_audio}")
            continue

        # Ajustar la duración del audio al tiempo de la frase
        try:
            audio_clip = ajustar_duracion_audio(nombre_archivo_audio, tiempo)
            print(f"Duración del audio ajustada correctamente para {nombre_archivo_audio}")
        except Exception as e:
            print(f"Error al ajustar la duración del audio para {nombre_archivo_audio}: {e}")
            continue

        # Verificar la duración del audio antes de continuar
        if audio_clip.duration == 0:
            print(f"Error: El clip de audio '{nombre_archivo_audio}' tiene duración cero.")
            continue

        # Crear el TextClip para la frase sin bg_color para permitir ver el fondo
        try:
            texto_clip = (TextClip(frase, fontsize=160, color='white', size=(1080, 1920), font='Impact', method='caption')
                          .set_duration(tiempo)
                          .fadein(1)
                          .set_position("center"))
            print(f"TextClip creado correctamente para la frase: {frase}")
        except Exception as e:
            print(f"Error al crear TextClip para la frase '{frase}': {e}")
            continue

        # Verificar la duración del TextClip
        if texto_clip.duration == 0:
            print(f"Error: El TextClip para la frase '{frase}' tiene duración cero.")
            continue

        # Añadir el audio ajustado al clip de texto
        try:
            video_con_audio = texto_clip.set_audio(audio_clip)
            print("Audio añadido al TextClip correctamente.")
        except Exception as e:
            print(f"Error al añadir audio al TextClip para la frase '{frase}': {e}")
            continue

        # Superponer el texto y el audio sobre el video de fondo
        try:
            video_fondo_clip = video_fondo.set_duration(tiempo)
            video_final_clip = CompositeVideoClip([video_fondo_clip, video_con_audio])
            print("CompositeVideoClip creado correctamente.")
        except Exception as e:
            print("Error al crear CompositeVideoClip:", e)
            continue

        # Exportar el video individual en formato MP4
        try:
            video_final_clip.write_videofile(nombre_archivo_video, fps=24)
            print(f"Video generado: {nombre_archivo_video}")
        except Exception as e:
            print(f"Error al escribir el archivo de video {nombre_archivo_video}: {e}")
            continue

        # Cargar el video exportado para asegurarnos de que se concatene correctamente
        try:
            clip_cargado = VideoFileClip(nombre_archivo_video)
            clips.append(clip_cargado)
        except Exception as e:
            print(f"Error al cargar el archivo de video {nombre_archivo_video} para la concatenación:", e)
            continue

        # Actualizar la barra de progreso
        progress_bar["value"] = index + 1
        root.update_idletasks()

    messagebox.showinfo("Éxito", "Todos los videos individuales han sido generados correctamente.")
    return clips




# Función para combinar todos los videos individuales en un solo video final
def combinar_videos(clips):
    # Concatenar todos los videos en uno solo
    video_final = concatenate_videoclips(clips, method="compose")
    output_path = "video_final_con_fondo.mp4"
    video_final.write_videofile(output_path, fps=24)
    print(f"Video final generado: {output_path}")
    messagebox.showinfo("Éxito", "El video final ha sido generado correctamente.")

def seleccionar_archivo(progress_bar, root):
    archivo_csv = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
    )
    print("Ruta del archivo CSV seleccionado:", archivo_csv)  # Depuración

    if archivo_csv:  # Verifica que el archivo CSV fue seleccionado
        video_fondo_path = filedialog.askopenfilename(
            title="Seleccionar archivo de video de fondo",
            filetypes=(("Archivos de Video", "*.mp4;*.mov;*.avi"), ("Todos los archivos", "*.*"))
        )
        print("Ruta del video de fondo seleccionado:", video_fondo_path)  # Depuración

        if video_fondo_path:  # Verifica que el video de fondo fue seleccionado
            try:
                # Intentar cargar el archivo CSV y comprobar si está bien cargado
                df = pd.read_csv(archivo_csv)
                print("Contenido del CSV cargado correctamente:", df.head())  # Muestra las primeras filas del CSV

                # Verificar que las columnas necesarias están presentes
                if 'frase' not in df.columns or 'tiempo' not in df.columns:
                    messagebox.showerror("Error", "El archivo CSV debe contener las columnas 'frase' y 'tiempo'.")
                    print("Error: El archivo CSV no contiene las columnas requeridas 'frase' y 'tiempo'.")
                    return

                # Verificar que la columna 'tiempo' tiene datos numéricos
                if not pd.api.types.is_numeric_dtype(df['tiempo']):
                    messagebox.showerror("Error", "La columna 'tiempo' en el archivo CSV debe contener valores numéricos.")
                    print("Error: La columna 'tiempo' no es numérica.")
                    return

                # Asegurarse de que el archivo de video es accesible y compatible
                try:
                    video_fondo = VideoFileClip(video_fondo_path)
                    print("Video de fondo cargado correctamente:", video_fondo_path)
                except Exception as video_error:
                    messagebox.showerror("Error", f"No se pudo cargar el video de fondo: {video_error}")
                    print("Error al cargar el video de fondo:", video_error)
                    return

                # Si todo se carga correctamente, procede con el procesamiento
                progress_bar["value"] = 0  # Reiniciar la barra de progreso

                # Generar los videos individuales con el video de fondo y el texto superpuesto
                clips = generar_videos_individuales(df, video_fondo_path, progress_bar, root)

                # Combinar todos los videos individuales en un solo video final
                combinar_videos(clips)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")
                print("Error general al procesar el archivo:", e)
        else:
            messagebox.showerror("Error", "No se seleccionó un archivo de video de fondo.")
            print("Error: No se seleccionó un archivo de video de fondo.")  # Depuración adicional
    else:
        messagebox.showerror("Error", "No se seleccionó un archivo CSV.")
        print("Error: No se seleccionó un archivo CSV.")  # Depuración adicional




# Configuración de la interfaz gráfica
def main():
    root = tk.Tk()
    root.title("Generador de Videos con Fondo y Frases")
    root.geometry("400x250")

    label = tk.Label(root, text="Generador de Videos con Frases", font=("Helvetica", 16))
    label.pack(pady=20)

    boton_seleccionar = tk.Button(root, text="Seleccionar Archivo CSV y Video de Fondo", font=("Helvetica", 14),
                                  command=lambda: seleccionar_archivo(progress_bar, root))
    boton_seleccionar.pack(pady=10)

    # Barra de progreso
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
