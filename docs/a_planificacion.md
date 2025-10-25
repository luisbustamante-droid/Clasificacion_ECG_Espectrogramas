## 1. Definición del problema y objetivos

Las arritmias cardíacas constituyen uno de los principales problemas de salud pública a nivel mundial, siendo responsables de una proporción significativa de muertes súbitas y complicaciones cardiovasculares. Su detección oportuna y precisa a partir de electrocardiogramas (ECG) es fundamental para la prevención y manejo clínico de los pacientes, sin embargo, el análisis manual de las señales requiere tiempo, experiencia y puede estar sujeto a error humano.
Los sistemas automáticos de clasificación basados en aprendizaje profundo (deep learning) han demostrado gran capacidad para identificar patrones complejos en señales biomédicas, pero a menudo adolecen de falta de interpretabilidad, lo que dificulta su adopción clínica. Asimismo, muchos modelos se entrenan sobre bases de datos con sesgos de representación o sin mecanismos de trazabilidad que permitan justificar las decisiones del sistema.
En este contexto, el problema central que aborda este proyecto es cómo desarrollar un modelo de inteligencia artificial capaz de clasificar distintos tipos de arritmias cardíacas de manera precisa y explicable, a partir de señales de ECG transformadas en espectrogramas. Se busca que el modelo no solo optimice métricas de rendimiento, sino que también ofrezca interpretaciones visuales comprensibles para profesionales de la salud.

**Objetivo general:**
Desarrollar y evaluar un prototipo de inteligencia artificial capaz de clasificar arritmias cardíacas en cinco clases AAMI a partir de espectrogramas de señales de ECG, utilizando CNNs preentrenadas y técnicas de explicabilidad, logrando un rendimiento mínimo de F1 macro ≥ 0.80 en conjunto de prueba independiente por paciente.

**Objetivos específicos:**

- Preparar y segmentar el dataset MIT-BIH Arrhythmia Database según protocolo AAMI, garantizando separación por paciente para evitar fuga de información.
Transformar ventanas de ECG en espectrogramas STFT reproducibles (224×224 px), asegurando uniformidad y normalización para entrenamiento.
- Entrenar un modelo baseline con ResNet50 y un modelo ligero con MobileNetV2, empleando transferencia de aprendizaje y regularización, con reportes de métricas de validación.
- Incorporar Grad-CAM para explicar las decisiones de los modelos.
- Evaluar el prototipo en conjunto de prueba independiente por paciente, con métricas F1 macro, verificando que se cumplen los criterios de éxito establecidos.
- Desarrollar una aplicación web para la implementación y uso de esta herramienta que permita el diagnóstico médico.

**Justificación de la relevancia del proyecto**

El desarrollo de herramientas automáticas y explicables para la detección de arritmias representa un aporte significativo tanto en el ámbito clínico como en el científico. Desde una perspectiva médica, la capacidad de identificar de forma temprana alteraciones del ritmo cardíaco permite mejorar la precisión diagnóstica, reducir la carga de trabajo de los cardiólogos y facilitar la monitorización remota de pacientes, especialmente en contextos con recursos limitados o alta demanda asistencial.

Desde el punto de vista tecnológico, el proyecto aborda uno de los principales desafíos actuales en inteligencia artificial aplicada a la salud: la explicabilidad y confianza en los modelos de aprendizaje profundo. Al incorporar técnicas visuales de interpretación, el sistema propuesto ofrece transparencia y trazabilidad, favoreciendo su integración en flujos clínicos reales y fomentando la aceptación por parte del personal médico.

Asimismo, la utilización de bases de datos públicas y metodologías reproducibles contribuye al avance científico y a la creación de modelos abiertos, auditables y susceptibles de mejora continua. En conjunto, el proyecto no solo busca optimizar el desempeño técnico de la clasificación de arritmias, sino también establecer un marco ético, explicable y responsable para el uso de inteligencia artificial en la práctica médica, alineado con los principios de equidad, privacidad y seguridad de los datos biomédicos.

**Alcance (qué incluye y qué NO incluye)**

**Alcance incluido:**

- Procesamiento de señales de ECG del MIT-BIH Arrhythmia Database.
- Transformación de señales 1D en espectrogramas 2D mediante STFT.
- Implementación y entrenamiento de dos CNNs preentrenadas: ResNet50 (baseline) y MobileNetV2 (modelo ligero).
- Clasificación en cinco clases AAMI: N, SVEB, VEB, F, Q.
- Incorporación de explicabilidad con Grad-CAM, generando mapas de activación sobre espectrogramas.
- Evaluación cuantitativa con métricas estándar: F1 macro y sensibilidad por clase.
- Documentación final e informe técnico con resultados, interpretaciones y limitaciones.

**Alcance excluido:**

- Uso de otros datasets distintos al MIT-BIH.
- Inclusión de técnicas de ensemble, optimización exhaustiva de hiperparámetros o arquitecturas fuera de ResNet50/MobileNetV2.
- Validación clínica en entornos hospitalarios o pruebas con pacientes reales.

**Cronograma de desarrollo**

El cronograma de sprints del proyecto se estructuró en cuatro fases principales distribuidas a lo largo de seis semanas, con una duración aproximada de una a dos semanas por sprint. El Sprint 1 y el Sprint 2 estuvieron orientados al análisis exploratorio, preprocesamiento de las señales de ECG y diseño inicial del pipeline de transformación a espectrogramas. Posteriormente, el Sprint 3 se centró en la implementación y entrenamiento de los modelos basados en redes neuronales convolucionales (CNN), así como en la integración de las métricas de desempeño y equidad. Finalmente, el Sprint 4 correspondió a la etapa de validación, generación de explicaciones mediante Grad-CAM y documentación técnica del sistema.

Aunque el plan inicial contemplaba una duración homogénea entre los sprints, el cronograma real presentó una variación durante el Sprint 4, el cual requirió más días de ejecución debido a la complejidad asociada con la interpretación de los resultados, la depuración del modelo y la preparación del informe final. Este ajuste no afectó significativamente el cumplimiento de los objetivos globales, pero permitió alcanzar una mayor estabilidad del modelo y una documentación más completa del proceso de desarrollo.

 **Recursos necesarios:**

En cuanto al hardware, se utilizaron equipos locales, principalmente laptops y computadoras personales, destinados al análisis exploratorio, entrenamiento de modelos y ejecución de pruebas controladas. Respecto al software, se hizo uso de herramientas y librerías de código abierto en el ecosistema de Python, incluyendo entornos de desarrollo como Jupyter Notebook, Google Colab y PyCharm, lo que permitió una implementación flexible, reproducible y sin dependencia de licencias propietarias. En el ámbito de la colaboración, se empleó GitHub como plataforma central para el control de versiones, gestión de código, documentación y trabajo colaborativo entre los miembros del equipo. Finalmente, en lo referente a los datos, se utilizaron datasets públicos ampliamente reconocidos en la investigación biomédica, principalmente la MIT-BIH Arrhythmia Database y la MIT-BIH 12-lead ECG Arrhythmia Database, garantizando la transparencia, accesibilidad y validez científica de las fuentes utilizadas.

**Riesgos identificados y mitigación**

1. Riesgos técnicos

Entre los riesgos técnicos destacan la variabilidad en la calidad de las señales de ECG, la escasez de ejemplos en clases minoritarias (especialmente la clase F) y las diferencias de frecuencia de muestreo entre las bases MIT-BIH Arrhythmia y Supraventricular Arrhythmia Database. Estos factores pueden afectar la estabilidad del modelo y su capacidad de generalización.

Estrategias de mitigación:

- Aplicación de filtros de preprocesamiento y normalización para homogeneizar las señales.
- Balanceo dirigido de las clases y ajuste de pesos en la función de pérdida (class weights).
- Evaluación con partición agrupada por paciente, evitando data leakage y sobreajuste.
- Validación cruzada y análisis de métricas por clase para identificar debilidades específicas.

2. Riesgos éticos y de sesgo

Las bases de datos utilizadas presentan limitaciones demográficas (predominio de adultos de ascendencia caucásica, registros de los años 70), lo que puede inducir sesgos de representación y afectar la equidad del modelo en poblaciones diversas.

Estrategias de mitigación:

- Reconocimiento explícito de los sesgos en la documentación técnica del proyecto.
- Uso de métricas de equidad (macro-F1 y F1 por clase) como indicadores principales de desempeño.
- Análisis de resultados orientado a la detección de comportamientos desiguales entre clases.
- Recomendación de validaciones adicionales con bases de datos más recientes y representativas antes de cualquier aplicación clínica.

3. Riesgos de privacidad y confidencialidad
Aunque los datos provienen de fuentes públicas, las señales de ECG constituyen información médica sensible. El manejo inadecuado de estos datos podría generar vulneraciones de privacidad.

Estrategias de mitigación:

- Uso exclusivo de bases de datos anonimizadas.
- Cumplimiento de buenas prácticas de seguridad y almacenamiento, conforme a lineamientos éticos y regulaciones internacionales (GDPR y CCPA).
- Restricción del uso del modelo a entornos académicos o de investigación, sin conexión a datos clínicos reales de pacientes.

4. Riesgos de mal uso o interpretación indebida

Existe el riesgo de que las salidas del modelo sean interpretadas como diagnósticos automáticos, o que se empleen en contextos clínicos sin supervisión médica, lo cual podría tener consecuencias adversas para los pacientes.

Estrategias de mitigación:

- Inclusión de advertencias explícitas sobre las limitaciones del modelo y su carácter de herramienta de apoyo.
- Implementación de un módulo de explicabilidad (Grad-CAM/Grad-CAM++) que permita visualizar las razones detrás de cada decisión.
- Promoción de un uso responsable, bajo la supervisión de profesionales de la salud y con fines exclusivamente educativos o de investigación.

