# CNNS Spectrograms: Clasificación de Arritmias ECG con Espectrogramas STFT

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)  
![PyTorch](https://img.shields.io/badge/PyTorch-2.3+-red.svg)  
![License](https://img.shields.io/badge/License-MIT-green.svg)  
![Status](https://img.shields.io/badge/Status-Active-success.svg)  

Proyecto de investigación y desarrollo para la detección y clasificación automática de arritmias cardíacas a partir de señales ECG, utilizando espectrogramas de tiempo-frecuencia como representación intermedia y redes convolucionales profundas (CNNs) preentrenadas.

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

## Descripción del problema
El proyecto aborda la detección de arritmias cardíacas mediante el análisis automático de señales de ECG (electrocardiograma). El desafío principal es el alto desbalance de clases —ciertos tipos de latidos (como “S” y “F”) son extremadamente raros en los registros—, lo que dificulta el entrenamiento estable y la generalización del modelo.

Este trabajo propone un enfoque basado en espectrogramas de tiempo-frecuencia para capturar patrones morfológicos y temporales de cada latido, facilitando el aprendizaje por redes convolucionales profundas.

**Usuarios objetivo:** investigadores biomédicos, profesionales de ingeniería biomédica y desarrolladores de sistemas de diagnóstico asistido.

## Dataset
**Fuentes principales:**  
- MIT-BIH Arrhythmia Database (PhysioNet)  
- SVDB (MIT-BIH Supraventricular Arrhythmia Database)

**Licencia:** PhysioNet Open Data License.  
**Frecuencia de muestreo:** 360 Hz  
**Duración típica de los registros:** 30 minutos por sujeto  
**Clases (según estándar AAMI):**  
`N` (Normal), `S` (Supraventricular), `V` (Ventricular), `F` (Fusion), `Q` (Indeterminado / Artefacto)

**Preprocesamiento aplicado:**
- Mapeo de símbolos MIT-BIH → clases AAMI  
- Ventaneo deslizante (2.5 s con paso de 0.5 s)  
- Cálculo de espectrogramas STFT (224×224 px) por ventana  
- División estratificada en train / val / test, excluyendo datos sintéticos  
- SMOTE 1D exclusivo para clase F (solo en TRAIN, post-split)  
- Almacenamiento en caché de imágenes (`spec_cache_224/{split}/{db}/{row_id}.png`)

## Metodología
**Arquitecturas CNN empleadas:**
- ResNet-50  
- MobileNetV3-Large  
- EfficientNetV2-B0  

**Preentrenamiento:** pesos de ImageNet.  
**Capa final:** reemplazada por clasificador `Linear` con Dropout ajustable (0.2-0.4).  
**Pérdida:** `ClassBalancedFocalLoss` con label smoothing y pesos inversos a la frecuencia de clases.  
**Optimizador:** `AdamW`  
**Scheduler:** `CosineAnnealingWarmRestarts`  
**Técnicas de robustez:**  
- AMP (Mixed Precision Training)  
- EMA (Exponential Moving Average) de parámetros  
- Gradient clipping y detección anti-NaN  
- WeightedRandomSampler con refuerzo selectivo de clases minoritarias (`minority_boost`)

**Métricas de evaluación:**
- F1-score (macro)  
- Accuracy  
- `classification_report` con control de clases ausentes  
- Matrices de confusión (normalizadas)

## Resultados
| Modelo                | F1 (Val) | F1 (Test) | Accuracy (Val) | Accuracy (Test) |
|-----------------------|----------|-----------|----------------|-----------------|
| **ResNet-50 (Cosine)**        | 0.49     | 0.56      | 0.84           | 0.86            |
| **MobileNetV3-Large**         | 0.52     | 0.58      | 0.86           | 0.88            |
| **EfficientNetV2-B0**         | 0.54     | 0.59      | 0.87           | 0.89            |

*(Valores representativos de ejecuciones controladas con datasets balanceados mediante SMOTE F)*

Los modelos basados en espectrogramas superan ampliamente a baselines puramente temporales, mostrando mejor sensibilidad en clases minoritarias `S` y `F`.

## Instalación y uso
### Requisitos del sistema
- Python ≥ 3.10  
- PyTorch ≥ 2.3  
- CUDA (opcional, recomendado)  
- Dependencias: `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `tqdm`, `opencv-python`, `wfdb`, `timm`

### Instalación
```bash
git clone https://github.com/tuusuario/cnns-spectrograms.git
cd cnns-spectrograms
pip install -r requirements.txt
