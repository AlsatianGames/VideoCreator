from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, VideoFileClip, concatenate_videoclips, concatenate_audioclips
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS  # Parche para compatibilidad con MoviePy

import pyttsx3
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

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
        silence_duration = duracion_objetivo - duracion_audio
        silence = AudioFileClip("C:/Users/Taliex4/Documents/Codigo/VideoCreator/silence.mp3").set_duration(silence_duration)
        audio_clip = concatenate_audioclips([audio_clip, silence])
    return audio_clip.set_duration(duracion_objetivo)

# Función para generar los clips de texto y audio para cada frase sin el fondo
def generar_clips_individuales(df, progress_bar, root):
    clips = []
    total = len(df)
    progress_bar["maximum"] = total

    # Crear la carpeta para almacenar los audios de frases
    nombre_carpeta = "audios_frases"
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)

    for index, row in df.iterrows():
        frase = row['frase']
        tiempo = float(row['tiempo'])

        # Generar el archivo de audio para la frase
        nombre_archivo_audio = os.path.join(nombre_carpeta, f"audio_frase_{index+1}.mp3")
        generar_audio(frase, nombre_archivo_audio)

        # Ajustar la duración del audio al tiempo de la frase
        audio_clip = ajustar_duracion_audio(nombre_archivo_audio, tiempo)

        # Crear el TextClip para la frase sin fondo
        texto_clip = (TextClip(frase, fontsize=160, color='white', size=(1080, 1920), font='Impact', method='caption')
                      .set_duration(tiempo)
                      .fadein(1)
                      .set_position("center"))

        # Añadir el audio ajustado al clip de texto
        video_con_audio = texto_clip.set_audio(audio_clip)
        clips.append(video_con_audio)

        # Actualizar la barra de progreso
        progress_bar["value"] = index + 1
        root.update_idletasks()

    messagebox.showinfo("Éxito", "Todos los clips individuales han sido generados correctamente.")
    return clips

# Función para combinar todos los clips individuales y superponer el fondo
def combinar_videos(clips, video_fondo_path, progress_bar, root, status_label):
    # Convertir la barra de progreso a modo indeterminado
    progress_bar["mode"] = "indeterminate"
    progress_bar.start()

    # Crear una función para ejecutar la exportación en un hilo separado
    def exportar_video():
        # Concatenar todos los videos de frases en uno solo
        video_frases = concatenate_videoclips(clips, method="compose")

        # Cargar el video de fondo y ajustar su duración para que coincida con el video de frases
        video_fondo = VideoFileClip(video_fondo_path).resize((1080, 1920)).set_opacity(0.1)
        video_fondo = video_fondo.set_duration(video_frases.duration)

        # Superponer el video de fondo y el video de frases
        video_final = CompositeVideoClip([video_fondo, video_frases])
        output_path = "video_final_con_fondo.mp4"

        # Exportar el video final
        video_final.write_videofile(output_path, fps=24)

        # Detener la barra de progreso y actualizar el mensaje de estado en la interfaz principal
        root.after(0, lambda: finalizar_proceso(progress_bar, status_label, output_path))

    # Iniciar el proceso de exportación en un hilo separado
    threading.Thread(target=exportar_video).start()

def finalizar_proceso(progress_bar, status_label, output_path):
    # Detener la barra de progreso y actualizar el mensaje de estado
    progress_bar.stop()
    progress_bar["mode"] = "determinate"
    progress_bar["value"] = 100  # Deja la barra llena para indicar que terminó
    status_label.config(text="Completado el proceso correctamente")
    print(f"Video final generado: {output_path}")
    messagebox.showinfo("Éxito", "El video final ha sido generado correctamente.")

# Función para seleccionar el archivo CSV y el video de fondo
def seleccionar_archivo(progress_bar, root, status_label):
    archivo_csv = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
    )
    print("Ruta del archivo CSV seleccionado:", archivo_csv)

    if archivo_csv:
        video_fondo_path = filedialog.askopenfilename(
            title="Seleccionar archivo de video de fondo",
            filetypes=(("Archivos de Video", "*.mp4;*.mov;*.avi"), ("Todos los archivos", "*.*"))
        )
        print("Ruta del video de fondo seleccionado:", video_fondo_path)

        if video_fondo_path:
            try:
                df = pd.read_csv(archivo_csv)
                if 'frase' not in df.columns or 'tiempo' not in df.columns:
                    messagebox.showerror("Error", "El archivo CSV debe contener las columnas 'frase' y 'tiempo'.")
                    return

                # Reiniciar la barra de progreso
                progress_bar["value"] = 0
                status_label.config(text="Generando clips individuales...")

                # Generar los clips individuales sin el fondo
                clips = generar_clips_individuales(df, progress_bar, root)

                # Cambiar mensaje de estado
                status_label.config(text="Generando video final, por favor espere...")
                root.update_idletasks()

                # Combinar todos los clips individuales con el fondo
                combinar_videos(clips, video_fondo_path, progress_bar, root, status_label)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")
        else:
            messagebox.showerror("Error", "No se seleccionó un archivo de video de fondo.")
    else:
        messagebox.showerror("Error", "No se seleccionó un archivo CSV.")

# Configuración de la interfaz gráfica
def main():
    root = tk.Tk()
    root.title("Generador de Videos con Fondo y Frases")
    root.geometry("400x300")

    label = tk.Label(root, text="Generador de Videos con Frases", font=("Helvetica", 16))
    label.pack(pady=10)

    boton_seleccionar = tk.Button(root, text="Seleccionar Archivo CSV y Video de Fondo", font=("Helvetica", 14),
                                  command=lambda: seleccionar_archivo(progress_bar, root, status_label))
    boton_seleccionar.pack(pady=10)

    # Barra de progreso
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    # Etiqueta de estado para mostrar mensajes debajo de la barra de progreso
    status_label = tk.Label(root, text="", font=("Helvetica", 12))
    status_label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
