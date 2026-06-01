import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

# Importar tus módulos personalizados
from modules.image_loader import load_image
from modules.preprocessing import extract_rois, grayscale_and_blur
from modules.segmentation import segment_upper, segment_lower
from modules.morphology import clean_mask
from modules.counting import count_panels
from modules.evaluation import evaluate

# =========================================================
# CONFIGURACIÓN DE LA PÁGINA WEB
# =========================================================
st.set_page_config(
    page_title="Contador de Paneles Solares - Unimagdalena",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ Proyecto de Segmentación de Imágenes de Dron")
st.markdown("""
Esta aplicación web presenta el flujo de procesamiento paso a paso, modelando la imagen aérea como una **señal discreta bidimensional**, aplicando técnicas de filtrado espacial, operaciones no lineales de amplitud y morfología matemática.
""")

# Justificación técnica (Teoría de señales)
with st.expander("📘 Fundamentos de Señales Espaciales (Justificación Técnica)"):
    st.markdown("""
    **Marco Teórico - Procesamiento de Señales I**
    
    Para este análisis sobre el edificio docente de la Universidad del Magdalena, la imagen se aborda formalmente como una **señal discreta bidimensional**, donde cada píxel es una muestra espacial.
    
    * **Filtrado Espacial (Pasa-bajas):** Antes de la segmentación, se aplica un suavizado Gaussiano. En el dominio de las frecuencias, esto actúa como un filtro pasa-bajas que atenúa el ruido de alta frecuencia (variaciones bruscas), estabilizando la señal.
    * **Umbralización (Operación no lineal):** La segmentación es una operación no lineal sobre la amplitud de la señal espacial. Se utilizó una estrategia híbrida (adaptativa y global) para contrarrestar los cambios de iluminación y sombras.
    * **Morfología Matemática:** Funciona como un filtro espacial no lineal de post-procesamiento para rellenar discontinuidades y separar frecuencias espaciales adyacentes (paneles muy juntos).
    
    *Desarrollado por: Camilo Cantillo, Luis Mercado*
    """)

# =========================================================
# BARRA LATERAL (SIDEBAR) 
# =========================================================
st.sidebar.header("⚙️ Panel de Control")

opcion_imagen = st.sidebar.selectbox(
    "1. Selección de Imagen:",
    ["DJI_0612.JPG (Predeterminada)", "DJI_0613.JPG"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
nombre_archivo = "DJI_0613.JPG" if "0613" in opcion_imagen else "DJI_0612.JPG"
image_path = os.path.join(BASE_DIR, "images", nombre_archivo)

img_ready = os.path.exists(image_path)

if img_ready:
    st.sidebar.success(f"⚡ Procesando en tiempo real: {nombre_archivo}")
else:
    st.sidebar.error(f"No se encontró '{nombre_archivo}'")

st.sidebar.divider()
st.sidebar.subheader("2. Ajuste de Umbrales Globales")
threshold_sup = st.sidebar.slider("Umbral ROI Superior (Sol)", 0, 255, 81)
threshold_inf = st.sidebar.slider("Umbral ROI Inferior", 0, 255, 90)
area_min
