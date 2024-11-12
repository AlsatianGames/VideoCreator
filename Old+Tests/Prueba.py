from moviepy.editor import TextClip, CompositeVideoClip
import pandas as pd

# Leer el archivo CSV
def leer_csv(archivo_csv):
    return pd.read_csv(archivo_csv)

# Función para crear un video con letras apareciendo gradualmente y fondo transparente
def generar_videos(df):
    for index, row in df.iterrows():
        frase = row['frase']
        tiempo = float(row['tiempo'])

        # Crear un TextClip con transparencia (sin color de fondo)
        def texto_progresivo(get_frame, t):
            # Calcular cuántas letras mostrar en función del tiempo t
            num_letras = int(len(frase) * (t / tiempo))
            # Crear un TextClip que solo muestra las letras calculadas
            return TextClip(frase[:num_letras], fontsize=160, color='white', font='Impact', size=(1080, 1920), method='caption', transparent=True).get_frame(t)

        # Crear el clip de video que va a mostrar progresivamente las letras
        texto_clip = TextClip("", fontsize=160, color='white', size=(1080, 1920), method='caption', transparent=True)
        texto_animado = texto_clip.fl(texto_progresivo)

        # Establecer la duración del video
        texto_animado = texto_animado.set_duration(tiempo)

        # Exportar el video con canal alpha (transparencia) usando el códec PNG en formato MOV
        nombre_archivo = f"video_frase_{index+1}.mp4"
        texto_animado.write_videofile(nombre_archivo, fps=24, codec='png', ffmpeg_params=["-pix_fmt", "rgba"])
        print(f"Video generado: {nombre_archivo}")

# Función principal
def main():
    archivo_csv = "C:\\Users\\Taliex4\\Documents\\Codigo\\frases.csv"  # Nombre del archivo CSV con las frases y tiempos
    df = leer_csv(archivo_csv)
    generar_videos(df)

if __name__ == "__main__":
    main()
