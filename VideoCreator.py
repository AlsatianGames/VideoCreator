from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
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

# Función para crear un video con letras animadas y con sonido
def generar_videos(df, progress_bar, root):
    total = len(df)
    progress_bar["maximum"] = total

    for index, row in df.iterrows():
        frase = row['frase']
        tiempo = float(row['tiempo'])

        # Crear la carpeta para cada frase
        nombre_carpeta = "frases"
        if not os.path.exists(nombre_carpeta):
            os.makedirs(nombre_carpeta)

        # Ruta de los archivos dentro de la carpeta
        nombre_archivo_audio = os.path.join(nombre_carpeta, f"audio_frase_{index+1}.mp3")
        nombre_archivo_video = os.path.join(nombre_carpeta, f"video_frase_{index+1}.mp4")

        # Generar el archivo de audio
        generar_audio(frase, nombre_archivo_audio)

        # Crear un TextClip con animación de desvanecimiento y fuente Impact
        texto_clip = (TextClip(frase, fontsize=160, color='white', size=(1080, 1920), font='Impact', method='caption', bg_color='black')
                      .set_duration(tiempo)
                      .fadein(1))  # Aplicar el efecto de fade in durante 1 segundo

        # Establecer la duración del video
        texto_clip = texto_clip.set_duration(tiempo)

        # Añadir el audio al video
        audio_clip = AudioFileClip(nombre_archivo_audio)
        video_con_audio = texto_clip.set_audio(audio_clip)

        # Exportar el video en formato MP4 dentro de la carpeta
        video_con_audio.write_videofile(nombre_archivo_video, fps=24)
        print(f"Video generado: {nombre_archivo_video}")

        # Actualizar la barra de progreso
        progress_bar["value"] = index + 1
        root.update_idletasks()

    messagebox.showinfo("Éxito", "Todos los videos han sido generados correctamente.")

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
            generar_videos(df, progress_bar, root)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo CSV: {e}")

# Configuración de la interfaz gráfica
def main():
    root = tk.Tk()
    root.title("Generador de Videos")
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
