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
