# Clasificación explicable de arritmias cardíacas a partir de electrocardiogramas transformados en espectrogramas mediante redes neuronales convolucionales

## Resumen
Este proyecto aborda la detección y clasificación de arritmias cardíacas a partir de señales de ECG crudas, transformadas en representaciones tiempo–frecuencia (espectrogramas), y analizadas con redes neuronales convolucionales (CNN). Se persigue un enfoque **explicable** que permita interpretar qué patrones del espectrograma sustentan las decisiones del modelo, aportando trazabilidad clínica y robustez metodológica.

## Objetivos
- **O1.** Construir un *pipeline* reproducible que convierta segmentos de ECG crudos en **espectrogramas**.
- **O2.** Entrenar y comparar tres arquitecturas CNN de referencia (**ResNet**, **MobileNet**, **EfficientNet**) para clasificación de arritmias.
- **O3.** Incorporar técnicas de **explicabilidad** (p. ej., Grad-CAM) para visualizar regiones relevantes en los espectrogramas.
- **O4.** Evaluar con métricas centradas en clases minoritarias (macro-F1, F1 por clase) y con **partición 70/15/15** estratificada y **agrupada por registro/paciente** para evitar *data leakage*.

## Contribución
1. **Pipeline extremo a extremo** desde ECG crudo → espectrograma → entrenamiento → explicabilidad.
2. **Evaluación justa** con división 70/15/15 sin fuga entre conjuntos (agrupación por `record_id`/paciente).
3. **Análisis comparativo** entre ResNet, MobileNet y EfficientNet con el mismo preprocesamiento.
4. **Explicabilidad** mediante mapas de activación sobre espectrogramas para interpretación clínica.

## Conjunto de datos
Se emplea **MIT-BIH Arrhythmia Database** (PhysioNet), accedido localmente desde `./mit-bih-arrhythmia-database-1.0.0`. El uso incluye:
- Lectura de señales y anotaciones (WFDB).
- Segmentación por latidos o ventanas deslizantes (p. ej., 2.5–5 s).
- Etiquetado según taxonomía AAMI u otra definida en el proyecto.
> Nota: se normalizarán frecuencias de muestreo y amplitudes para asegurar consistencia entre registros.

## Metodología (vista general)
1. **Preprocesamiento**: (opcional) filtrado banda 0.5–40 Hz y corrección de línea base; normalización por ventana.
2. **Representación**: cálculo de **espectrogramas** (p. ej., STFT/CWT), escala logarítmica y reescalado a tamaño estándar (p. ej., 224×224).
3. **Modelado**: *fine-tuning* de **ResNet**, **MobileNet** y **EfficientNet** (entrada 3 canales; el espectrograma en gris se replica a 3 canales).
4. **Entrenamiento**: **CrossEntropy** con **pesos por clase**, optimizador AdamW, *early stopping* por macro-F1.
5. **Evaluación**: accuracy, **macro-F1**, F1 por clase, matriz de confusión; reporte por clases AAMI.
6. **Explicabilidad**: Grad-CAM/Grad-CAM++ para visualizar regiones discriminativas del espectrograma.
7. **Reproducibilidad**: semillas fijadas, guardado de *splits*, pesos y *configs*.

## Partición de datos
Se aplicará una división **70%/15%/15%** con:
- **Estratificación por clase** (mantener proporciones).
- **Agrupación por `record_id`/paciente** (ningún registro se repite en train/val/test).

## Métricas y validación
- **Métrica principal**: **macro-F1** en validación/test.
- **Métricas secundarias**: F1 por clase, accuracy y matriz de confusión.