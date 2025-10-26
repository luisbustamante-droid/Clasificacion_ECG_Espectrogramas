# CNNS Spectrograms: Clasificación de Arritmias ECG con Espectrogramas STFT

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)  
![PyTorch](https://img.shields.io/badge/PyTorch-2.3+-red.svg)  
![License](https://img.shields.io/badge/License-MIT-green.svg)  
![Status](https://img.shields.io/badge/Status-Active-success.svg)  

Proyecto de investigación y desarrollo para la detección y clasificación automática de arritmias cardíacas a partir de señales ECG, utilizando espectrogramas de tiempo-frecuencia como representación intermedia y redes convolucionales profundas (CNNs) preentrenadas.

---

## Tabla de Contenidos
1. [Descripción del problema](#descripción-del-problema)  
2. [Dataset](#dataset)  
3. [Metodología](#metodología)  
4. [Resultados](#resultados)  
5. [Instalación y uso](#instalación-y-uso)  
6. [Interfaz de usuario](#interfaz-de-usuario)  
7. [Estructura del proyecto](#estructura-del-proyecto)  
8. [Consideraciones éticas](#consideraciones-éticas)  
9. [Autores y contribuciones](#autores-y-contribuciones)  
10. [Licencia](#licencia)  
11. [Agradecimientos y referencias](#agradecimientos-y-referencias)  

---

## Descripción del problema
El proyecto aborda la detección de arritmias cardíacas mediante el análisis automático de señales de ECG (electrocardiograma).  
El principal desafío es el **alto desbalance de clases**, ya que ciertos tipos de latidos (como `S` y `F`) son extremadamente raros, lo que dificulta el entrenamiento estable y la generalización.

Este trabajo propone un enfoque basado en **espectrogramas STFT** (Short-Time Fourier Transform) para capturar patrones morfológicos y temporales de cada latido, facilitando el aprendizaje mediante CNNs preentrenadas.

**Usuarios objetivo:** investigadores biomédicos, ingenieros biomédicos y desarrolladores de sistemas de diagnóstico asistido.

---

## Dataset
**Fuentes principales:**  
- **MIT-BIH Arrhythmia Database** (PhysioNet)  
- **SVDB (MIT-BIH Supraventricular Arrhythmia Database)**  

**Licencia:** PhysioNet Open Data License  
**Frecuencia de muestreo:** 360 Hz  
**Duración promedio:** 30 minutos por registro  
**Clases (según estándar AAMI):**  
`N` (Normal), `S` (Supraventricular), `V` (Ventricular), `F` (Fusión), `Q` (Indeterminado / Artefacto)

**Preprocesamiento aplicado:**
- Mapeo MIT-BIH → AAMI  
- Ventaneo deslizante (2.5 s, paso = 0.5 s)  
- Cálculo de espectrogramas STFT (224×224 px)  
- División estratificada train / val / test (sin datos sintéticos)  
- **SMOTE 1D** exclusivo para clase F (solo en *train*, post-split)  
- Caché persistente de imágenes (`spec_cache_224/{split}/{db}/{row_id}.png`)

---

## Metodología
**Arquitecturas CNN empleadas:**
- **ResNet-50**  
- **MobileNetV3-Large**  
- **EfficientNetV2-B0**

**Preentrenamiento:** pesos de *ImageNet*  
**Capa final:** `Linear` + `Dropout` (0.2–0.4)  
**Función de pérdida:** `ClassBalancedFocalLoss` con *label smoothing* y pesos inversos a la frecuencia de clases  
**Optimizador:** `AdamW`  
**Scheduler:** `CosineAnnealingWarmRestarts`  
**Técnicas de robustez:**  
- AMP (*Mixed Precision Training*)  
- EMA (Exponential Moving Average) de parámetros  
- Gradient clipping + control anti-NaN  
- `WeightedRandomSampler` con refuerzo moderado (`minority_boost ≈ 5–8`)  

**Métricas de evaluación:**  
- Macro F1-Score  
- Accuracy  
- `classification_report` robusto ante clases ausentes  
- Matrices de confusión normalizadas

---

## Resultados

### Rendimiento comparativo de modelos CNN

| Modelo                | Macro F1 (Val) | Macro F1 (Test) | Accuracy (Val) | Accuracy (Test) |
|-----------------------|----------------|------------------|----------------|-----------------|
| **ResNet-50 (Cosine)**       | 0.6138 | 0.6121 | 0.8361 | 0.8038 |
| **MobileNetV3-Large**        | 0.6907 | 0.6277 | 0.9127 | 0.8046 |
| **EfficientNetV2-B0**        | **0.7013** | **0.6495** | **0.9348** | **0.8327** |

Los modelos basados en **espectrogramas STFT** logran una mejora sustancial sobre métodos puramente temporales, mostrando **mayor sensibilidad en las clases minoritarias `S` y `F`**.  
EfficientNetV2-B0 alcanzó el mejor equilibrio entre precisión global y generalización.

---

## Instalación y uso

### Requisitos
- Python ≥ 3.10  
- PyTorch ≥ 2.3  
- CUDA (recomendado)  
- Dependencias: `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `tqdm`, `opencv-python`, `wfdb`, `timm`
