from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, VideoFileClip, concatenate_videoclips, concatenate_audioclips
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

# Función para crear videos individuales para cada frase con texto y audio
def generar_videos_individuales(df, progress_bar, root):
    clips = []
    total = len(df)
    progress_bar["maximum"] = total

    # Crear la carpeta para almacenar los videos de frases
    nombre_carpeta = "videos_frases"
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)

    for index, row in df.iterrows():
        frase = row['frase']
        tiempo = float(row['tiempo'])

        # Rutas de los archivos de audio y video
        nombre_archivo_audio = os.path.join(nombre_carpeta, f"audio_frase_{index+1}.mp3")
        nombre_archivo_video = os.path.join(nombre_carpeta, f"video_frase_{index+1}.mp4")

        # Generar el archivo de audio para la frase
        generar_audio(frase, nombre_archivo_audio)

        # Ajustar la duración del audio al tiempo de la frase
        audio_clip = ajustar_duracion_audio(nombre_archivo_audio, tiempo)

        # Crear el TextClip para la frase
        texto_clip = (TextClip(frase, fontsize=160, color='white', size=(1080, 1920), font='Impact', method='caption', bg_color='black')
                      .set_duration(tiempo)
                      .fadein(1))

        # Añadir el audio ajustado al clip de texto
        video_con_audio = texto_clip.set_audio(audio_clip)

        # Exportar el video individual en formato MP4
        video_con_audio.write_videofile(nombre_archivo_video, fps=24)
        print(f"Video generado: {nombre_archivo_video}")

        # Cargar el video exportado para asegurarnos de que se concatene correctamente
        clip_cargado = VideoFileClip(nombre_archivo_video)
        clips.append(clip_cargado)

        # Actualizar la barra de progreso
        progress_bar["value"] = index + 1
        root.update_idletasks()

    messagebox.showinfo("Éxito", "Todos los videos individuales han sido generados correctamente.")
    return clips

# Función para combinar todos los videos individuales en un solo video final
def combinar_videos(clips):
    # Concatenar todos los videos en uno solo
    video_final = concatenate_videoclips(clips, method="compose")
    output_path = "video_final_con_frases.mp4"
    video_final.write_videofile(output_path, fps=24)
    print(f"Video final generado: {output_path}")
    messagebox.showinfo("Éxito", "El video final ha sido generado correctamente.")

# Función para seleccionar el archivo CSV
def seleccionar_archivo(progress_bar, root):
    archivo_csv = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
    )

    if archivo_csv:
        try:
            df = pd.read_csv(archivo_csv)
            progress_bar["value"] = 0  # Reiniciar la barra de progreso

            # Generar los videos individuales
            clips = generar_videos_individuales(df, progress_bar, root)

            # Combinar todos los videos individuales en un solo video final
            combinar_videos(clips)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")

# Configuración de la interfaz gráfica
def main():
    root = tk.Tk()
    root.title("Generador de Videos con Frases")
    root.geometry("400x250")

    label = tk.Label(root, text="Generador de Videos con Frases", font=("Helvetica", 16))
    label.pack(pady=20)

    boton_seleccionar = tk.Button(root, text="Seleccionar Archivo CSV", font=("Helvetica", 14),
                                  command=lambda: seleccionar_archivo(progress_bar, root))
    boton_seleccionar.pack(pady=10)

    # Barra de progreso
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
