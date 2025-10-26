## 1. Análisis de sesgos

**¿El dataset tiene sesgos demográficos, culturales o de otro tipo?**

El modelo fue entrenado con un conjunto de datos combinado de los datasets MIT-BIH Arrhythmia Database y MIT-BIH Supraventricular Arrhythmia Database. Estas bases de datos presentan algunos sesgos estructurales, demográficos y técnicos que condicionan tanto el aprendizaje del modelo como la generalización de sus predicciones.

En primer lugar, las bases originales poseen sesgos demográficos y culturales debido a que los registros fueron obtenidos en el Beth Israel Hospital de Boston entre 1975 y 1979, a partir de una muestra limitada y geográficamente homogénea, conformada principalmente por pacientes adultos de ascendencia caucásica. La falta de diversidad étnica, etaria y de condiciones fisiológicas puede generar un sesgo del espectro electrocardiográfico humano. La falta de metadatos sobre variables sociodemográficas impide evaluar el comportamiento del modelo según subgrupos poblacionales, debido a esto, el sistema de clasificación puede mostrar rendimientos desiguales cuando se aplica a pacientes de otras regiones, edades o condiciones clínicas distintas a las representadas en el conjunto de entrenamiento.

En segundo lugar, el proyecto reconoce y aborda un sesgo de selección clínica presente en ambas bases de datos. La base MIT-BIH Arrhythmia incluye tanto registros aleatorios como registros elegidos intencionalmente para contener arritmias infrecuentes, lo que rompe la correspondencia con la prevalencia real de dichas condiciones. En cuanto a la base MIT-BIH Supraventricular Arrhythmia Database, fue diseñada para incrementar la presencia de arritmias supraventriculares (clase S), pero en su forma original mantenía una sobrerrepresentación de latidos normales, lo que inicialmente provocó un desempeño deficiente del modelo (F1 = 0.1 para las clases minoritarias). Ante este desequilibrio, se implementó un balanceo dirigido del conjunto de datos, seleccionando únicamente los registros correspondientes a arritmias raras dentro de la base supraventricular. Esta decisión metodológica permitió incrementar la proporción efectiva de ejemplos de la clase S y mejorar significativamente las métricas globales de desempeño (F1 =0.8). Pese a esta mejora cuantitativa, persisten limitaciones derivadas de la escasez extrema de ciertas clases, como la clase F (fusiones de latido normal y ventricular), cuya baja frecuencia dificulta el aprendizaje robusto de sus patrones espectrales. Este fenómeno evidencia la existencia de un sesgo de escasez o infrarrepresentación, que puede conducir a errores sistemáticos de clasificación.

A nivel técnico, se identifican además sesgos de dominio y de instrumentación. Las diferencias en frecuencia de muestreo entre bases, 360 Hz en MIT-BIH Arrhythmia y 128 Hz en la Supraventricular, junto con las variaciones en el tipo de equipo y calidad de registro, generan discrepancias en la resolución espectral y en la textura visual de los espectrogramas. Estos factores pueden inducir a las CNN a aprender características asociadas al dispositivo o al ruido, en lugar de patrones fisiológicos genuinos, afectando la transferencia del modelo hacia entornos modernos.



**¿Cómo podrían afectar estos sesgos las predicciones?**

Estos sesgos podrían afectar a la calidad de las predicciones en varios aspectos. En primer lugar, pueden provocar una asimetría en la sensibilidad por clase, donde las arritmias raras, aunque más representadas tras la corrección, siguen siendo clasificadas con menor precisión. En segundo lugar, se pueden dar sesgos demográficos, ya que el modelo podría rendir mejor en sujetos adultos de características similares a los datos históricos y peor en poblaciones pediátricas, geriátricas o de distinta composición étnica. 

**¿Qué grupos podrían ser perjudicados?**

Los grupos que podrían ser perjudicados son aquellos cuya fisiología cardiaca difiere significativamente del patrón predominante en el conjunto de entrenamiento, es decir, pacientes pediátricos, mujeres cuyas características electrocardiográficas pueden diferir en amplitud y frecuencia, personas mayores con comorbilidades o sujetos de distintas etnias. También podrían verse afectados quienes utilicen dispositivos modernos de monitoreo cardíaco, en los cuales el ruido, la frecuencia de muestreo y la calidad de señal difieren de las condiciones originales de los años setenta.

## 2. Equidad y Fairness

**¿El modelo trata a todos los grupos de forma equitativa?**

El modelo propuesto busca garantizar un tratamiento equitativo de las diferentes categorías diagnósticas de arritmia, entendiendo la equidad no únicamente en términos demográficos, sino también como uniformidad en el desempeño entre clases. Dado que las bases MIT-BIH Arrhythmia Database y MIT-BIH Supraventricular Arrhythmia Database carecen de información demográfica explícita como edad, sexo y etnia, por lo que la equidad no puede evaluarse directamente a nivel poblacional. De manera general, se reconoce la limitación estructural de estos datos, lo que podría afectar la generalización del modelo fuera del contexto original. En cuanto al análisis, se centró en la equidad interclase, es decir, en que el modelo ofreciera un rendimiento equilibrado entre las distintas clases de arritmias. Tras una corrección del conjunto de datos para mejorar la representación de las clases raras, se observó un aumento significativo del desempeño balanceado. Con un macro-F1 de 0.8, indicador de que el modelo aprendió a tratar las clases de forma más justa.

**Métricas de fairness evaluadas:**

Para evaluar la equidad en el desempeño, se utilizaron métricas centradas en la uniformidad interclase, entre ellas:
1.	Macro-F1: principal métrica del proyecto, ya que pondera de igual manera todas las clases sin depender de su frecuencia.
2.	F1 por clase: permite detectar clases con comportamientos atípicos o subrepresentadas.
3.	Matriz de confusión: utilizada como herramienta visual para evidenciar desbalances residuales en la clasificación.
El uso del macro-F1 como métrica principal refleja una decisión metodológica orientada a la equidad: el modelo no busca maximizar la precisión global o accuracy, sino asegurar un rendimiento homogéneo entre todas las clases.

**Estrategias implementadas para mitigar inequidades:**

Con el objetivo de mejorar la equidad del modelo y reducir los efectos de la desproporción entre clases, se implementaron estrategias de mitigación en distintas fases del pipeline:
•	Curación dirigida del dataset, eliminando la sobreabundancia de registros normales e incrementando la presencia de clases raras (especialmente S).
•	Reponderación de la función de pérdida (class weights en CrossEntropyLoss), para equilibrar la contribución de cada clase durante el entrenamiento.
•	Partición estratificada y agrupada por paciente (70/15/15), garantizando que cada subconjunto mantuviera una distribución proporcional de clases y evitando fugas de información.
Si bien estas estrategias mejoraron la equidad técnica del modelo, la clase F continúa mostrando un rendimiento inferior debido a su escasez en las bases originales. 

## 3. Privacidad

**¿Se utilizan datos personales o sensibles?**

El proyecto utiliza datos biomédicos provenientes de dos repositorios de acceso público ampliamente reconocidos, ambas mantenidas por el Massachusetts Institute of Technology (MIT) y el Beth Israel Hospital dentro del repositorio PhysioNet. Estas bases contienen señales de electrocardiograma anotadas por expertos, pero no incluyen información personal identificable, como nombre, edad, dirección, historia clínica ni otros datos demográficos vinculables a la identidad de los pacientes. Si bien las señales de ECG son consideradas datos biomédicos sensibles ya que provienen de seres humanos y reflejan información fisiológica única, las versiones públicas de las bases MIT-BIH han sido anonimizadas y desidentificadas conforme a los estándares de protección de datos utilizados en investigación médica. Son registros clínicos anonimizados empleados exclusivamente con fines científicos.

**¿Cómo se protege la privacidad de los usuarios?**

La protección de la privacidad en este proyecto se garantiza desde el origen mismo de los datos. Las bases MIT-BIH provienen de un proceso de anonimización completa, en el cual se eliminaron todos los metadatos personales y se codificaron los registros únicamente mediante identificadores numéricos (record_id). Además, las bases están alojadas en el repositorio PhysioNet, que exige el cumplimiento de un acuerdo de uso ético de datos biomédicos antes de su descarga, restringiendo su utilización a fines académicos o clínicos no comerciales.

**Cumplimiento con regulaciones (GDPR, CCPA, etc.)**

Aunque las bases MIT-BIH fueron recolectadas con anterioridad a las regulaciones modernas de protección de datos, su formato y uso actual en investigación cumplen con los principios fundamentales del Reglamento General de Protección de Datos (GDPR) de la Unión Europea y la California Consumer Privacy Act (CCPA) de Estados Unidos. En particular, se cumplen los siguientes criterios: anonimización irreversible, finalidad limitada al área científica y de investigación, minimización de datos y transparencia y trazabilidad garantizada por el portal PhysioNet.

## 4.	Transparencia y explicabilidad

**¿El modelo es interpretable?**

La interpretabilidad es un eje central en este proyecto. Dado que las redes neuronales convolucionales suelen ser percibidas como modelos de “caja negra”, se diseñó una arquitectura que integre mecanismos de explicabilidad visual, permitiendo comprender qué patrones dentro del espectrograma sustentan cada clasificación. El modelo es parcialmente interpretable: si bien la estructura interna de una CNN profunda no es directamente comprensible para el usuario final, la combinación de espectrogramas y técnicas de visualización de activaciones le da interpretabilidad. Se puede rastrear y visualizar qué regiones del espectrograma influyen en la decisión, ofreciendo una interpretación coherente con la fisiología del ECG.

**¿Los usuarios entienden cómo funciona?**

Aunque el modelo subyacente utiliza arquitecturas profundas, se diseñó el flujo metodológico para que los usuarios clínicos y técnicos puedan comprender las bases de su funcionamiento y verificar la validez de sus predicciones. La conversión de las señales de ECG a espectrogramas permite representar la información en un formato visual intuitivo, más accesible para profesionales de la salud familiarizados con patrones de frecuencia cardíaca. Las visualizaciones generadas mediante mapas de calor Grad-CAM se integran como herramienta de comunicación explicativa. Estas imágenes destacan las zonas del espectrograma donde la red neuronal concentró su atención durante la clasificación, facilitando al usuario la interpretación clínica del resultado. 

**Técnicas de explicabilidad implementadas (SHAP, LIME, etc.):**

Para abordar la explicabilidad en redes convolucionales aplicadas a espectrogramas, se implementaron métodos basados en gradientes y visualización de activaciones:
-	Grad-CAM: técnica que calcula el gradiente de la clase predicha respecto a los mapas de activación de las últimas capas convolucionales, generando un mapa de calor que resalta las regiones del espectrograma más relevantes para la decisión del modelo.
-	Grad-CAM++: extensión de Grad-CAM que pondera las contribuciones de cada píxel de manera más precisa, ofreciendo mapas con mejor localización espacial, especialmente útiles cuando existen múltiples regiones activas.
Estas técnicas fueron seleccionadas por su compatibilidad con arquitecturas CNN y su capacidad para generar explicaciones visuales intuitivas sin alterar el modelo base. Aunque herramientas como SHAP o LIME son ampliamente utilizadas en otros contextos de explicabilidad, su aplicación directa sobre espectrogramas resulta menos interpretativa, razón por la cual se priorizaron métodos de visualización directa basados en gradientes.

## 5.	Impacto social

**¿Qué impacto positivo puede tener el proyecto?**

El desarrollo de este sistema tiene un alto potencial de impacto social y sanitario positivo, especialmente en el fortalecimiento del diagnóstico temprano y la atención oportuna de enfermedades cardiovasculares, que constituyen la principal causa de mortalidad a nivel mundial. El proyecto puede mejorar la eficiencia y precisión del diagnóstico clínico, al ser una herramienta de apoyo a la decisión que puede asistir a profesionales de la salud en la detección de arritmias cardiacas. Al ser explicable, garantiza que las decisiones del modelo puedan ser interpretadas y validadas por cardiólogos, reduciendo la incertidumbre relacionada a los sistemas de caja negra. El uso de espectrogramas y modelos CNN optimizados permite reducir la brecha tecnológica entre entornos hospitalarios avanzados y lugares de atención primaria, generando el acceso equitativo a tecnologías de diagnóstico asistido por IA. 

**¿Qué impactos negativos podrían surgir?**

En cuanto a los posibles impactos negativos, uno de los principales riesgos es la posibilidad de errores de clasificación que conduzcan a interpretaciones diagnósticas incorrectas, especialmente en clases minoritarias o mal representadas, como la clase F. Aunque el modelo no reemplaza al criterio clínico, el uso inadecuado de esta herramienta podría generar consecuencias clínicas indeseadas. Otro impacto negativo potencial es el sesgo de generalización, ya que el modelo fue entrenado sobre bases históricas con características demográficas y tecnológicas específicas. Aplicarlo directamente en otras poblaciones o con equipos modernos podría reducir su desempeño, afectando la equidad diagnóstica entre diferentes grupos de pacientes.

**¿Quiénes se benefician? ¿Quiénes podrían ser perjudicados?**

Los principales beneficiarios del proyecto son los pacientes y profesionales de la salud. Los pacientes se benefician al acceder a diagnósticos más rápidos, precisos y explicables, lo que puede traducirse en intervenciones tempranas y una reducción en la mortalidad por arritmias. Los profesionales médicos, al contar con una herramienta complementaria que refuerza la toma de decisiones, reduce la carga laboral y proporciona evidencias visuales claras para la interpretación clínica.  Las instituciones hospitalarias y académicas pueden beneficiarse también de esta herramienta, ya que el pipeline reproducible permite adaptar la metodología a distintos contextos y dispositivos ECG, potenciando la investigación y el desarrollo de más sistemas de IA médica.
En cuanto a los posibles perjudicados, podrían ser los pacientes de grupos poblacionales no representados en los datos originales, sobre los cuales el modelo podría mostrar menor desempeño diagnóstico. También podría verse afectado el personal clínico si se implementa el sistema sin una capacitación adecuada, lo que generaría desconfianza o malinterpretación de las salidas del modelo.

## 6. Responsabilidad

**¿Quién es responsable si el modelo falla?**

La responsabilidad frente a posibles fallos del modelo se distribuye entre los diferentes roles del equipo, promoviendo la corresponsabilidad y la trazabilidad de cada decisión técnica y ética. El Product Owner define la visión del producto y prioriza los objetivos clínicos para garantizar que el modelo responda a necesidades reales del usuario final. El Scrum Master asegura el cumplimiento de los principios de transparencia, promoviendo prácticas éticas y comunicación efectiva entre los equipos técnico y clínico. Mientras que el Development Team, asume la responsabilidad técnica del modelo, incluyendo su implementación, calidad, integridad de datos y mejora continua. En caso de un fallo en el modelo, la responsabilidad se aborda colectivamente, siguiendo el principio de responsabilidad compartida y aprendizaje iterativo característico de Scrum. Cada iteración permite detectar errores, evaluar sus causas y definir acciones correctivas de manera colaborativa, sin desplazar la responsabilidad al individuo sino al proceso de desarrollo.

**¿Qué mecanismos de accountability existen?**

El proyecto adopta diversos mecanismos de accountability orientados a asegurar la transparencia técnica y ética del sistema a lo largo de su ciclo de vida.
-	Documentación exhaustiva del pipeline: todos los pasos del flujo de trabajo se registran mediante scripts reproducibles, configuración versionada y almacenamiento de logs de entrenamiento, garantizando la trazabilidad experimental.
-	Explicabilidad y auditabilidad: las técnicas de Grad-CAM y Grad-CAM++ implementadas permiten auditar visualmente las decisiones del modelo, mostrando qué regiones del espectrograma fueron determinantes para cada predicción. 
-	Evaluación con métricas centradas en la equidad: la adopción de métricas como el macro-F1 y el F1 por clase asegura que el rendimiento sea evaluado de forma justa, evitando la sobreoptimización hacia clases dominantes y promoviendo un comportamiento equilibrado.

**Plan de monitoreo y actualización del modelo:**

El proyecto contempla un plan de monitoreo continuo del desempeño y comportamiento del modelo, orientado a mantener su validez y confiabilidad a lo largo del tiempo, especialmente en caso de ser adaptado a nuevos entornos clínicos o poblaciones distintas a las del entrenamiento original.
-	Monitoreo de desempeño: se recomienda evaluar periódicamente las métricas de rendimiento en nuevos conjuntos de datos clínicos, con el fin de detectar posibles degradaciones en la precisión o aparición de sesgos poblacionales.
-	Control de versiones y trazabilidad: todas las versiones del modelo, sus hiperparámetros y pesos entrenados deben almacenarse bajo control de versiones, permitiendo reproducir y auditar cualquier resultado retrospectivamente.
-	Revisión ética continua: todo despliegue o actualización deberá contar con la aprobación de un comité ético institucional, que evalúe el impacto potencial en pacientes, la equidad del desempeño y la transparencia de las explicaciones generadas.

## 7. Uso dual y mal uso

**¿Podría el modelo usarse con fines maliciosos?**

El modelo fue diseñado y desarrollado con fines médicos y de investigación. Se trata de un sistema capaz de clasificar arritmias a partir de espectrogramas de ECG, un uso indebido podría implicar:
-	Diagnóstico incorrecto fuera de entornos clínicos, generando alarma innecesaria o decisiones médicas inapropiadas por personal no calificado.
-	Explotación de datos sensibles si el modelo se aplica sin protocolos de anonimización, comprometiendo la privacidad de los pacientes.
-	Investigación maliciosa sobre patrones cardíacos que podría ser utilizada en contextos no éticos, por ejemplo, para discriminación laboral o aseguradora basada en riesgo cardiovascular.
Aunque el modelo en sí no genera daño directamente, su implementación fuera de un contexto controlado podría acarrear consecuencias adversas para individuos y grupos poblacionales.

**¿Qué salvaguardas se han implementado?**

Para mitigar estos riesgos, se han incorporado estrategias de protección. Una de ellas es la restricción de acceso a los datos y modelos, los pesos entrenados y los conjuntos de datos se mantienen en repositorios controlados. Por otro lado, mediante la documentación de buenas prácticas, se han definido protocolos de uso que especifican que el modelo es únicamente un sistema de apoyo clínico, y no sustituye la evaluación profesional. Estas medidas buscan asegurar que el modelo se utilice de manera ética, segura y dentro de los límites para los que fue diseñado.

**Limitaciones de uso:**

-	El modelo no debe emplearse como diagnóstico independiente, sino como apoyo complementario para profesionales médicos.
-	Su desempeño puede variar según la población y el dispositivo de adquisición de ECG, por lo que se recomienda validación local antes de su implementación clínica.
-	La clase F aún presenta baja representatividad, y por lo tanto las predicciones en esta categoría son menos confiables.
-	No se garantiza la ausencia de sesgos en poblaciones no representadas en las bases MIT-BIH originales, por ejemplo, grupos etarios, étnicos o con comorbilidades específicas.

## 8. Limitaciones reconocidas

**¿En qué casos NO debe usarse el modelo?**

El modelo desarrollado no debe emplearse como herramienta única de diagnóstico médico, ni sustituir la valoración de un profesional de la salud. El modelo no está diseñado para pacientes con condiciones cardíacas complejas que no se encuentran representadas en las bases de datos MIT-BIH, como ciertos síndromes congénitos o arritmias asociadas a múltiples comorbilidades. No debe utilizarse para la evaluación de registros obtenidos en dispositivos o configuraciones de ECG distintas a las empleadas durante el entrenamiento, dado que las diferencias en la adquisición podrían modificar las características del espectrograma y comprometer la precisión de la predicción. Tampoco está pensado para la toma de decisiones clínicas críticas sin la supervisión de un profesional calificado, especialmente en contextos de urgencia o tratamientos de alto riesgo.

**¿Qué advertencias deben darse a los usuarios?**

Se deben comunicar claramente varias advertencias a los usuarios del modelo. En primer lugar, aunque el modelo proporciona recomendaciones basadas en patrones aprendidos, la interpretación final debe ser realizada por un cardiólogo o profesional de la salud calificado. Además, las predicciones no son infalibles, por lo que siempre se debe considerar la posibilidad de falsos negativos o positivos, especialmente en el caso de arritmias raras o clases con baja representatividad. La confiabilidad del modelo también depende de la calidad de la señal de ECG; artefactos, ruido o registros incompletos pueden afectar negativamente su desempeño. 

**Casos límite donde el modelo no es confiable**

Existen escenarios específicos en los que la confianza del modelo disminuye. En primer lugar, las clases minoritarias, como la clase F, presentan muy pocos registros, lo que hace que las predicciones para este tipo de arritmia sean poco confiables. En segundo lugar, poblaciones no representadas en los registros MIT-BIH, como niños, adultos mayores extremos o ciertos grupos étnicos, pueden generar resultados sesgados. Además, la presencia de artefactos en los ECG, ya sea por ruido eléctrico, movimiento del paciente o colocación incorrecta de los electrodos, puede alterar los espectrogramas y provocar predicciones erróneas. El modelo no está validado para su aplicación fuera del entorno clínico, como en uso doméstico o entornos no supervisados, donde la interpretación profesional no está disponible, lo que limita su confiabilidad en estos contextos.

## Referencias Bibliográficas:
•	J. Beck y A. John, "Explainable AI (XAI) for Arrhythmia detection from electrocardiograms," arXiv, 2025. [Online]. Available: https://arxiv.org/abs/2508.17294
•	E. Nasarian, R. Alizadehsani, U. R. Acharya y K.-L. Tsui, "Designing Interpretable ML System to Enhance Trust in Healthcare: A Systematic Review to Proposed Responsible Clinician-AI-Collaboration Framework," arXiv, 2023. [Online]. Available: https://arxiv.org/abs/2311.11055
•	E. C. Chukwu y P. A. Moreno-Sánchez, "Enhancing Arrhythmia Diagnosis with Data-Driven Methods: A 12-Lead ECG-Based Explainable AI Model," Proceedings of the 14th Supporting Health by Technology Conference 2025, Universidad de Twente, 2024. [Online]. Available: https://research.utwente.nl/en/publications/explainable-ai-xai-for-arrhythmia-detection-in-ecg
•	S. Mulukuntla, "Generative AI - Benefits, Limitations, Potential risks and Challenges in Healthcare Industry," International Journal of Medical and Health Science, vol. 8, no. 4, p. 211, 2025. [Online]. Available: https://doi.org/10.53555/eijmhs.v8i4.211
•	Z. Weizman, "Critical Limitations in Systematic Reviews of Large Language Models in Health Care," Journal of Medical Internet Research, vol. 27, e81769, 2025. [Online]. Available: https://doi.org/10.2196/81769
•	Reuters, "It's too easy to make AI chatbots lie about health information, study finds," 1-Jul-2025. [Online]. Available: https://www.reuters.com/business/healthcare-pharmaceuticals/its-too-easy-make-ai-chatbots-lie-about-health-information-study-finds-2025-07-01/
•	The Guardian, "Advanced AI suffers 'complete accuracy collapse' in face of complex problems, study finds," 9-Jun-2025. [Online]. Available: https://www.theguardian.com/technology/2025/jun/09/apple-artificial-intelligence-ai-study-collapse
•	Reddit, "Dual-Use Technologies & Their Misuse: A Double-Edged Sword," 6-Jan-2025. [Online]. Available: https://www.reddit.com/r/ObscurePatentDangers/comments/1huzgx6
