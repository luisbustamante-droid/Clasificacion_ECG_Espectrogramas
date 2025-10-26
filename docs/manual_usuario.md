## 1. Pantalla de Inicio de Sesión

La aplicación cuenta con un sistema básico de autenticación para controlar el acceso a los módulos de análisis y generación de reportes.

### Descripción general

Al ejecutar la aplicación o acceder mediante el enlace web, se muestra la siguiente pantalla:
<img width="1920" height="1080" alt="login" src="https://github.com/user-attachments/assets/0b66ab34-271c-4261-a1da-f2bd38de008d" />

### Elementos de la interfaz

| Elemento | Descripción |
|-----------|-------------|
| **Campo “Usuario”** | Permite ingresar el nombre de usuario autorizado. |
| **Campo “Contraseña”** | Permite ingresar la contraseña; incluye un botón de visualización de texto (icono de ojo). |
| **Botón “Entrar”** | Envía las credenciales para acceder a los módulos del sistema. |

### Credenciales de acceso

Para fines de prueba o demostración, se utilizan las siguientes credenciales:

* Usuario: user

* Contraseña: password

### Flujo de acceso

1. Ingrese las credenciales en los campos correspondientes.  
2. Presione **“Entrar”**.  
3. Si los datos son correctos, se redirige automáticamente al módulo **Inicio**.  
4. En caso de error, el sistema mostrará un mensaje de autenticación inválida.

---

## 2. Módulo de Inicio

El módulo **Inicio** constituye la pantalla principal del sistema y ofrece una **visión general del proyecto**, sus objetivos y las bases de datos empleadas.  
Desde aquí el usuario puede comprender el propósito de la aplicación antes de acceder a los módulos de análisis técnico o clínico.


<img width="1920" height="1080" alt="Screenshot (416)" src="https://github.com/user-attachments/assets/39ea1be7-2b0b-4583-b9ff-83c2b8bd7d75" />

### Elementos de la interfaz

| Elemento | Descripción |
|-----------|-------------|
| **Descripción del sistema** | Explica los objetivos: clasificación de arritmias, interpretación clínica y comparación de arquitecturas CNN. |
| **Secciones principales** | Resumen de los tres módulos disponibles y su propósito. |
| **Explorador del dataset y señal ECG** | Presenta la información técnica de las bases MIT-BIH y SVDB (origen, frecuencia de muestreo, canales y propósito). |

### Explorador interactivo de señal ECG

<img width="1920" height="1080" alt="Screenshot (417)" src="https://github.com/user-attachments/assets/e07991dc-c3fd-48d0-893d-064bab572a14" />


Esta sección permite **visualizar señales reales de ECG** provenientes de las bases de datos MIT-BIH y SVDB, con controles interactivos.

| Control | Descripción |
|----------|-------------|
| **Base de datos** | Selector para elegir entre *MIT-BIH Arrhythmia Database* o *SVDB*. |
| **Registro** | Permite seleccionar el número del registro ECG a visualizar. |
| **Duración de ventana (s)** | Control deslizante para definir la longitud de la ventana de señal mostrada. |
| **Inicio de la ventana (s)** | Control para desplazar la señal y analizar diferentes segmentos. |
| **Gráfica de señal ECG** | Muestra la señal cruda del canal MLII, representando la amplitud (mV) en función del tiempo (s). |


### Interpretación

Este módulo **no realiza inferencia ni clasificación**, sino que cumple una función **informativa y exploratoria**, ideal para:

- Familiarizarse con la estructura de las bases de datos.  
- Visualizar características morfológicas del ECG (ondas P, QRS, T).  
- Comprobar la correcta lectura de registros WFDB antes del análisis automático.

**Nota:**  
La visualización interactiva emplea los mismos parámetros de segmentación utilizados por el modelo CNN, garantizando consistencia entre los datos mostrados y los espectrogramas empleados durante el entrenamiento.

---

## 3. Módulo: Informe Técnico

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1eb4a0e2-1785-4866-afbd-d1dbc0ae92ea" />

### Descripción general

El módulo **Informe Técnico** permite al usuario consultar los resultados obtenidos durante el entrenamiento y evaluación de los modelos de clasificación de arritmias.

### Funciones principales

- **Visualizar los objetivos del modelo** y una breve descripción de la arquitectura utilizada (por defecto, *EfficientNetV2-B0*).  
- **Revisar los conjuntos de datos empleados**, incluyendo información de los registros MIT-BIH y SVDB.  
- **Examinar las configuraciones del pipeline**, como número de épocas, tamaño de lote, tasa de aprendizaje y funciones de pérdida.  
- **Observar las métricas de rendimiento** (Accuracy, F1-score macro y por clase AAMI) en los conjuntos de validación y prueba.  
- **Consultar las limitaciones y observaciones** del modelo, como posibles fuentes de error o restricciones del sistema.  
- **Explorar metadatos y distribución de latidos**, mediante tablas y gráficos que muestran la frecuencia de clases dentro de los registros ECG.

### Navegación

1. Desde el menú lateral, seleccione **“Informe Técnico”**.  
2. La pantalla se actualizará mostrando la información estructurada por secciones (Objetivo, Conjuntos de Datos, Resultados del Modelo, etc.).  
3. Puede desplazarse verticalmente para recorrer cada sección.  
4. En la parte inferior, podrá visualizar la tabla de metadatos y el gráfico de distribución de latidos por clase.

### Propósito

Este módulo está diseñado para **consultar y analizar los resultados técnicos del modelo**, facilitando la interpretación del rendimiento y la comprensión general del sistema antes de ejecutar la inferencia clínica.

---

## 4. Módulo: Informe Clínico

El módulo **Informe Clínico** constituye la sección más importante de la aplicación, donde se realiza la **predicción automática de arritmias cardíacas** a partir de señales de ECG reales.  
Permite cargar registros de prueba del sistema o subir archivos externos en formato WFDB comprimidos en un archivo `.zip`.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/54439161-1329-459c-90f6-79354c1a8a72" />

---

### Descripción general

El módulo ofrece dos modalidades para ingresar los datos:

1. **Selección de registro predefinido**  
   - El usuario puede escoger directamente uno de los registros de prueba incluidos (por ejemplo, `MITDB_108` o `SVDB_821`).
   - El sistema carga automáticamente la señal ECG asociada al registro y la prepara para el análisis.

<img width="763" height="394" alt="Screenshot 2025-10-26 123935" src="https://github.com/user-attachments/assets/07ba2ed5-1d0f-4b62-ad29-5a812c02a8b8" />


2. **Carga de archivo ZIP externo**  
   - Se admite la carga manual de registros en formato **WFDB comprimido (.zip)**, que deben contener los archivos `.dat`, `.hea` y `.atr`.  
   - Al presionar **“Browse files”**, se abrirá el explorador de archivos para seleccionar el registro a analizar.

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/445c994a-96ff-4e18-b000-095b246b1628" />


---

### Ejecución de la predicción

Una vez cargada la señal, el usuario debe presionar el botón **“Predecir”**.  
Durante la ejecución, se mostrará una **barra de progreso** que indica el avance del proceso de análisis.

El sistema realiza automáticamente las siguientes tareas:

- **Normalización de la señal ECG** y truncamiento a 30 segundos (para optimizar el procesamiento).  
- **Detección automática de R-peaks**, puntos característicos del ciclo cardíaco.  
- **Extracción de ventanas de 5 segundos** centradas en los R-peaks detectados.  
- **Conversión de cada ventana a espectrogramas STFT (224×224 px)**.  
- **Inferencia mediante el modelo CNN entrenado (EfficientNetV2-B0 por defecto)**.

---

### Visualización de resultados

Tras el procesamiento, el sistema muestra:

- **Predicción global del registro**, indicando la clase AAMI más probable (N, S, V, F o Q) junto con su porcentaje de confianza.  
- **Interpretación clínica** asociada a la clase detectada.  
- **Visualización de detalle**:
  - **Señal cruda** centrada en el R-peak de mayor relevancia.
  - **Grad-CAM superpuesto** que indica las regiones de la señal que más influyeron en la clasificación.

<img width="1649" height="660" alt="Screenshot 2025-10-26 122306" src="https://github.com/user-attachments/assets/6503ff05-9f24-4d8b-aadf-d04ddd9bbd8a" />


---

### Interpretación de la salida

| Elemento | Descripción |
|-----------|-------------|
| **Predicción del registro** | Clase AAMI predicha y porcentaje de confianza. |
| **Mensaje clínico** | Breve explicación del tipo de arritmia detectada (por ejemplo, “Clase S: Supraventricular”). |
| **Gráfica de señal cruda** | Segmento temporal centrado en el latido más relevante. |
| **Mapa Grad-CAM** | Proyección de atención sobre el espectrograma, resaltando la zona con mayor influencia del modelo. |

**Nota importante:**  
Los resultados tienen carácter **informativo** y no constituyen un diagnóstico médico.  
Se recomienda su uso como **herramienta de apoyo** en la interpretación de señales ECG.


### Recomendaciones de uso

- Asegúrese de que el archivo ZIP no supere los **200 MB**.  
- Los archivos deben incluir los tres componentes WFDB (`.dat`, `.hea`, `.atr`).  
- Para resultados más confiables, utilice registros con estructura compatible con las bases **MIT-BIH** o **SVDB**.  
- Si la predicción presenta baja confianza (<50 %), se recomienda analizar el registro completo o utilizar un modelo alternativo.

---

**Conclusión:**  
El módulo **Informe Clínico** integra todo el flujo de inferencia, desde la carga de la señal hasta la visualización interpretativa del resultado, brindando una experiencia clínica explicable y didáctica.


