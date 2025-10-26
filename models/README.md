# Resultados finales — Comparación de modelos CNN (AAMI 5 clases)

Los tres modelos se entrenaron bajo el mismo pipeline de espectrogramas STFT (224×224 px, 2.5 segundos por ventana centrada en R-peaks).  
La métrica principal utilizada fue **Macro F1-Score**, complementada con **Accuracy** para evaluar la consistencia global de las predicciones.

---

## 1. EfficientNetV2-B0

**Mejor época:** 10 / 15  
**Macro F1 (Validación):** 0.7013 | **Accuracy (Validación):** 0.9348  
**Macro F1 (Test):** 0.6495 | **Accuracy (Test):** 0.8327  

**Observaciones:**
- Presentó el mejor rendimiento global.
- Gran estabilidad y capacidad de generalización.
- Elevada sensibilidad en las clases **S** (supraventricular) y **F** (fusión).
- Modelo más adecuado para entornos clínicos de despliegue.

---

## 2. MobileNetV3-Large

**Mejor época:** 12 / 20  
**Macro F1 (Validación):** 0.6907 | **Accuracy (Validación):** 0.9127  
**Macro F1 (Test):** 0.6277 | **Accuracy (Test):** 0.8046  

**Observaciones:**
- Modelo liviano y eficiente, ideal para inferencia en tiempo real.
- Desempeño muy cercano al de EfficientNet, con menor costo computacional.
- Convergencia estable y robusta frente a datos combinados (MIT-BIH + SVDB).

---

## 3. ResNet-50

**Mejor época:** 6 / 6  
**Macro F1 (Validación):** 0.6138 | **Accuracy (Validación):** 0.8361  
**Macro F1 (Test):** 0.6121 | **Accuracy (Test):** 0.8038  

**Observaciones:**
- Modelo base sólido para comparación.
- Menor capacidad de generalización frente a EfficientNet y MobileNet.
- Tendencia al sobreajuste en clases minoritarias.

---

## Resumen comparativo

| Modelo              | F1 (Val) | Acc (Val) | F1 (Test) | Acc (Test) | Comentario principal                         |
|----------------------|:--------:|:----------:|:----------:|:------------:|-----------------------------------------------|
| **EfficientNetV2-B0** | **0.7013** | **0.9348** | **0.6495** | **0.8327** | Mejor desempeño global                        |
| **MobileNetV3-Large** | 0.6907 | 0.9127 | 0.6277 | 0.8046 | Eficiente y óptimo para inferencia rápida     |
| **ResNet-50**         | 0.6138 | 0.8361 | 0.6121 | 0.8038 | Baseline sólido, menor generalización         |

---

## Conclusión

El modelo **EfficientNetV2-B0** obtuvo los mejores resultados tanto en validación como en prueba, alcanzando un **Macro F1 de 0.70 (val)** y **0.65 (test)**, con **accuracy superior al 93 % en validación y 83 % en prueba**.  
Se consolida como la arquitectura óptima para la clasificación AAMI de arritmias en este pipeline de espectrogramas ECG.

El modelo **MobileNetV3-Large** constituye una alternativa ligera con excelente compromiso entre precisión y eficiencia, adecuada para aplicaciones en tiempo real.  
**ResNet-50** se mantiene como referencia comparativa en el análisis de desempeño entre arquitecturas profundas.
