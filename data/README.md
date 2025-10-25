# Proyecto CNNS Spectrograms — MIT-BIH + SVDB

Este proyecto implementa una arquitectura basada en **redes convolucionales (CNNs)** para la **detección automática de arritmias cardíacas** a partir de señales ECG.  
El enfoque central consiste en la conversión de segmentos de señal en **espectrogramas 2D** (imágenes), permitiendo aprovechar arquitecturas modernas de visión por computadora como **MobileNetV3**, **EfficientNet** y **ResNet**.

---

## 1. Conjuntos de datos utilizados

El modelo fue entrenado y evaluado a partir de la combinación de **dos bases de datos complementarias** provenientes de [PhysioNet](https://physionet.org/):

### MIT-BIH Arrhythmia Database (MITDB)
- **Fuente:** Beth Israel Hospital (Boston) y MIT Laboratory for Computational Physiology.  
- **Contenido:** 48 registros de aproximadamente 30 minutos de duración cada uno.  
- **Frecuencia de muestreo:** 360 Hz.  
- **Canales:** MLII y V1/V5 (solo se usa el canal MLII por consistencia).  
- **Etiquetado:** Cada complejo QRS está anotado y validado clínicamente.  
- **Norma empleada:** AAMI EC57 — estándar para evaluación de algoritmos de arritmias.  
- **Referencia:** [MIT-BIH Arrhythmia Database – PhysioNet](https://physionet.org/content/mitdb/1.0.0/)

### MIT-BIH Supraventricular Arrhythmia Database (SVDB)
- **Fuente:** Beth Israel Hospital (Boston).  
- **Contenido:** 78 registros de entre 30 y 60 minutos, con énfasis en arritmias **supraventriculares**.  
- **Frecuencia de muestreo:** 128 Hz (reescalada a 360 Hz para compatibilidad).  
- **Canales:** ECG único (normalmente MLII).  
- **Etiquetado:** Anotaciones clínicas con énfasis en latidos tipo **S (Supraventricular)**.  
- **Referencia:** [MIT-BIH Supraventricular Arrhythmia Database – PhysioNet](https://physionet.org/content/svdb/1.0.0/)

---

## 2. Estructura de los datos combinados

Los registros de ambos datasets fueron unificados y normalizados bajo un mismo esquema de muestreo y etiquetado, siguiendo la **clasificación AAMI EC57**.  
Cada latido (beat) se asocia a una de las cinco clases principales:

| Clase AAMI | Descripción | Ejemplo de símbolos MIT-BIH |
|:-----------:|:------------|:-----------------------------|
| **N** | Latido normal / bundle branch block | N, L, R |
| **S** | Latido supraventricular | A, a, J, S |
| **V** | Latido ventricular | V, E |
| **F** | Fusión de latido normal y ventricular | F |
| **Q** | Latido desconocido o artefacto | /, f, Q |

Cada beat fue procesado en una **ventana centrada en el R-peak** (≈2.5 s), garantizando contexto suficiente antes y después del complejo QRS.

---

## 3. Preprocesamiento y generación de espectrogramas

1. **Remuestreo:**  
   Todas las señales fueron remuestreadas a **360 Hz**.

2. **Normalización:**  
   Se aplicó normalización por z-score por registro (μ=0, σ=1).

3. **Extracción de ventanas:**  
   - Duración: **2.5 segundos** (900 muestras).  
   - Estride: 0.5 s entre ventanas consecutivas.  
   - Centrado en picos R detectados mediante algoritmos Pan–Tompkins optimizados.

4. **Espectrogramas STFT:**  
   - Transformada de Fourier de ventana corta (STFT).  
   - Tamaño de imagen: **224×224 px**.  
   - Escala log-magnitud, normalizada entre [0,1].  
   - Cada espectrograma se guarda como archivo PNG en `spec_cache_224/{split}/{db}/{row_id}.png`.

5. **División estratificada:**  
   - Estratificación por registro (`db_record_id`) excluyendo datos sintéticos.  
   - Splits fijos: **train / val / test**.  
   - El balanceo se realizó solo sobre el conjunto de **entrenamiento**.

---

## 4. Balanceo y aumentación de datos

Para mitigar la fuerte desproporción entre clases (especialmente **S** y **F**), se aplicaron técnicas de balanceo:

- **SMOTE 1D** (sólo para clase F en el split de entrenamiento).  
- Generación de espectrogramas sintéticos en `spec_cache_224/train/AUG/`.  
- **WeightedRandomSampler** con *minority_boost* reducido tras SMOTE.  
- Augmentaciones leves en entrenamiento:  
  - Variación de brillo/contraste.  
  - Ruido gaussiano.  
  - *Random resized crops* y *gain jitter* (Test-Time Augmentation opcional).

---

## 5. Etiquetas y metadatos

Cada fila del dataset consolidado incluye:

| Columna | Descripción |
|:--------|:-------------|
| `db` | Fuente de origen (MITDB o SVDB, o AUG para SMOTE) |
| `record_id` | Nombre original del registro (e.g., `101`, `8001`) |
| `db_record_id` | Identificador compuesto único (`MITDB_101`) |
| `beat_idx` | Índice del latido dentro del registro |
| `aami_class` | Clase AAMI (N, S, V, F, Q) |
| `split` | train / val / test |
| `spec_path` | Ruta al espectrograma 224×224 correspondiente |

---

## 6. Notas finales

- El conjunto combinado MITDB+SVDB permite cubrir un espectro más amplio de arritmias.  
- Los splits de validación y prueba se mantienen **sin SMOTE ni augmentación**.  
- La inferencia en la aplicación Streamlit utiliza **ventanas consecutivas** sin filtrado por tipo de base de datos, replicando condiciones reales de monitoreo ECG.


