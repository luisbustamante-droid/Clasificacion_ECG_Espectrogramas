# Clasificación explicable de arritmias cardíacas a partir de electrocardiogramas transformados en espectrogramas mediante redes neuronales convolucionales

## Introducción

Las arritmias cardíacas representan alteraciones en el ritmo normal del corazón y constituyen un problema clínico de gran relevancia debido a su impacto en la salud cardiovascular y la mortalidad asociada. La detección temprana y precisa de estas anomalías es esencial para el diagnóstico oportuno y la toma de decisiones médicas.

En este proyecto se desarrolla un sistema de **clasificación automática de arritmias** a partir del **MIT-BIH Arrhythmia Database**, utilizando señales de electrocardiograma (ECG). Para ello:

- Se extraen fragmentos de latidos individuales de los registros ECG.
- Dichos fragmentos se transforman en **espectrogramas** mediante técnicas de análisis tiempo-frecuencia (STFT).
- Los espectrogramas se emplean como entradas en una **red neuronal convolucional (CNN)** para la clasificación de los diferentes tipos de arritmia.
- Se incorporan métodos de **explicabilidad (XAI)**, como Grad-CAM, para interpretar la relevancia de las regiones espectrales en cada predicción.

El objetivo final es no solo lograr un buen rendimiento en la clasificación, sino también garantizar que el modelo proporcione **explicaciones comprensibles** que respalden la interpretación clínica de los resultados.

## Informe sobre la estructura del MIT-BIH Arrhythmia Database

### 1. Descripción general
El **MIT-BIH Arrhythmia Database** es un conjunto de registros de **electrocardiogramas (ECG)** ampliamente usado en investigación sobre arritmias.  
Características principales:
- **48 registros** de ~30 minutos cada uno.
- Cada registro contiene **2 canales (derivaciones)** de ECG.
- **Frecuencia de muestreo**: ~360 Hz.
- Incluye archivos de datos de señal, encabezados con metadatos y anotaciones manuales de expertos.

---

### 2. Archivos por registro
Para un registro, por ejemplo `100`, se encuentran típicamente:
- **100.dat** → Señal ECG en formato binario.
- **100.hea** → Header con información del registro (fs, canales, unidades).
- **100.atr** → Anotaciones de latidos y ritmos.

---

### 3. Canales (*channels*)
- *Channel* = **una derivación de ECG**.
- Cada registro tiene **2 canales** simultáneos, que pueden corresponder a derivaciones como:
  - MLII (Modified Lead II)
  - V5, V1, V2, III (dependiendo del registro)
- En Python con `wfdb`:
  - `record.p_signal.shape == (n_muestras, n_canales)`
  - Ejemplo: `sig = record.p_signal[:, 0]  # canal 0`

**Resumen**: un canal es simplemente una columna de la matriz de señal, es decir, una derivación distinta del ECG.

---

### 4. Contenido del header `.hea`
El archivo de encabezado describe cómo interpretar la señal:
- **fs**: frecuencia de muestreo.
- **nsig**: número de canales.
- Por canal:
  - **gain**: factor de conversión de digital a mV.
  - **baseline**: valor de referencia del ADC.
  - **units**: normalmente `mV`.
  - **sig_name**: nombre de la derivación (ej. MLII, V5).

---

### 5. Señales en WFDB
- **`record.p_signal`** → matriz en unidades físicas (mV).  
  *Recomendado para análisis.*
- **`record.d_signal`** → señal cruda en unidades digitales (ADC).
- **`record.fs`** → frecuencia de muestreo.
- **`record.sig_name`** → nombres de las derivaciones.

---

### 6. Anotaciones `.atr`
Con `wfdb.rdann(record, 'atr')` obtenemos:
- **`ann.sample`** → índice de muestra del latido (entero).
- **`ann.symbol`** → símbolo de la anotación (ej.: `N`, `V`, `A`, `F`).
- **`ann.aux_note`** → notas adicionales (ej. episodios de AFIB).
- **`ann.chan`** → canal asociado a la anotación.

---

### 7. Símbolos y clases AAMI
Los símbolos de latido se mapean a las clases estandarizadas de AAMI:

- **N**: normales y similares → `N, L, R, e, j`
- **S**: supraventriculares → `A, a, J, S`
- **V**: ventriculares → `V, E`
- **F**: fusión → `F`
- **Q**: otros → `/`, `f`, `Q`, `?`, `|`

Este mapeo permite reducir la complejidad a 5 clases principales: **N, S, V, F, Q**.

---

### 8. Variables en un dataset procesado
Al extraer latidos, se obtiene un `DataFrame` con:
- **Metadatos**
  - `record_id`: registro (ej. `"100"`).
  - `patient_id`: identificador del paciente (≈ record_id en MIT-BIH).
  - `fs`: frecuencia de muestreo.
  - `sample_index`: posición de la muestra del latido.
  - `mit_symbol`: símbolo original.
  - `aami_class`: clase agrupada AAMI.

- **Características de señal**
  - `amp_peak`: amplitud pico a pico.
  - `energy`: suma de cuadrados (energía).
  - `area`: integral bajo la curva.
  - `qrs_width_s`: ancho del QRS en segundos.
  - `mean_v`, `std_v`, `skew_v`, `kurt_v`: estadísticos.
  - `frag_len_samples`: longitud del fragmento extraído.

- **Calidad / anomalías**
  - `flag_saturation`: latido con amplitud extrema.
  - `flag_high_noise`: latido con desviación estándar muy alta.
  - `is_outlier`: outlier según IsolationForest.

---

### 9. Tiempo, muestras y ventanas
- Un latido está centrado en `sample_index`.
- Se extrae un **fragmento** alrededor (ej. −200 ms a +200 ms).
- Conversión: `tiempo (s) = sample_index / fs`.

---

### 10. Resumen práctico
- **Canal**: una derivación (columna de señal).
- **Muestra**: índice en la señal (convierte a tiempo con fs).
- **Latido**: anotación en `ann.sample` con símbolo en `ann.symbol`.
- **Clase**: `mit_symbol` → `aami_class`.
- **Header**: describe cómo convertir digital a físico y nombres de canales.
- **Split correcto**: por `record_id` o `patient_id` para evitar fuga.