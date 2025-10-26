# Ejecución de Pruebas Unitarias

Este proyecto incluye un conjunto de **tests automáticos** diseñados para verificar el correcto funcionamiento del pipeline de procesamiento ECG, los modelos CNN (EfficientNetV2-B0, MobileNetV3-Large y ResNet-50) y la aplicación de inferencia.

---

## Estructura de pruebas

```
tests/
├── test_data_processing.py   # Valida carga de datos, R-peaks y espectrogramas
├── test_model.py             # Verifica modelos CNN y checkpoints .pt
└── test_app.py               # Comprueba flujo de inferencia en la app
```

---

## Requisitos previos

1. Tener instalado **Python 3.9 o superior**.  
2. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```
3. Asegurar que los modelos entrenados estén en la carpeta `models/`:

   ```
   models/
   ├── efficientnet_v2_b0_best_ema.pt
   ├── mobilenet_v3_large_best_ema.pt
   └── resnet50_best_ema.pt
   ```

---

## Cómo ejecutar las pruebas

Desde la raíz del proyecto, simplemente ejecuta:

```bash
pytest -v
```

Esto buscará automáticamente todos los archivos que empiecen con `test_` dentro de la carpeta `tests/` y ejecutará cada uno.

---

## Comandos útiles

| Comando | Descripción |
|----------|--------------|
| `pytest -v` | Ejecuta todas las pruebas con salida detallada |
| `pytest -q` | Modo silencioso (solo muestra resultados) |
| `pytest -v --disable-warnings` | Oculta los warnings |
| `pytest tests/test_model.py -v` | Ejecuta solo las pruebas del modelo |
| `pytest tests/test_app.py::test_inference_pipeline -v` | Ejecuta una prueba específica |

---

## Resultado esperado

Si todas las pruebas son correctas, deberías ver algo como:

```
============================= test session starts =============================
collected 12 items

tests/test_data_processing.py ....                                   [ 33%]
tests/test_model.py ....                                             [ 66%]
tests/test_app.py ....                                               [100%]

======================== 12 passed in 5.12s =========================
```

---

## Notas

- Estas pruebas se ejecutan **sin necesidad de GPU**, ya que usan tensores aleatorios o señales pequeñas de prueba.  
- Los modelos `.pt` se cargan en modo `eval()` para evitar requerir entrenamiento.  
