# Tests Unitarios - Proyecto Rocket Mineria

Este directorio contiene todos los tests unitarios del proyecto de predicción de partidas de Rocket League.

## Estructura de Tests

```
tests/
├── test_preprocessing.py  # Tests de limpieza y features
├── test_model.py          # Tests del modelo y predicciones
├── test_api.py            # Tests de endpoints de la API
└── README.md              # Este archivo
```

## Cobertura de Tests

### test_preprocessing.py (20 tests)
- **TestCleaning**: Verificación de limpieza de datos
  - Conversión de fechas
  - Conversión de tipos
  - Integridad de datos
  - Manejo de valores nulos

- **TestFeatures**: Creación de features
  - Categorías de diferencia de goles
  - Buckets de duración
  - Indicador de partida competitiva
  - Feature combinada team_mode

- **TestDataIntegration**: Pipeline completo
  - Integración de limpieza y features
  - Calidad de datos final

### test_model.py (30+ tests)
- **TestModelLoading**: Carga de modelos y encoders
  - Existencia de archivos
  - Carga correcta
  - Métodos disponibles

- **TestModelPredictions**: Predicciones individuales
  - Forma de predicciones
  - Probabilidades
  - Clases válidas

- **TestBatchPredictions**: Predicciones en lote
  - Longitud correcta
  - Validez de predicciones

- **TestFeatureEngineering**: Ingeniería de features
  - One-hot encoding
  - Cálculo de features

- **TestModelMetrics**: Métricas y metadatos
  - Consistencia del modelo
  - Integridad de datos

### test_api.py (50+ tests)
- **TestNormalizationFunctions**: Funciones de normalización
  - Normalización de colores
  - Normalización de ganadores
  - Soporte multiidioma

- **TestRootEndpoint**: Endpoint raíz
  - Respuesta correcta
  - Información de endpoints
  - Estado del sistema

- **TestPredictEndpoint**: Endpoint de predicción
  - Predicciones válidas
  - Manejo de variantes de entrada
  - Validación de datos
  - Manejo de errores

- **TestGenerateSyntheticEndpoint**: Generación sintética
  - Parámetros por defecto
  - Filtros por modo de juego
  - Límites de generación

- **TestStatsEndpoint**: Estadísticas
  - Distribuciones
  - Métricas agregadas

- **TestAPIValidation**: Validación de entrada
  - Tipos de datos
  - Campos requeridos

- **TestAPIErrorHandling**: Manejo de errores
  - Errores internos
  - Mensajes de error

## Instalación

Instalar dependencias de testing:

```bash
pip install -r requirements-test.txt
```

## Ejecución de Tests

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests específicos

```bash
# Solo tests de preprocessing
pytest tests/test_preprocessing.py

# Solo tests del modelo
pytest tests/test_model.py

# Solo tests de la API
pytest tests/test_api.py
```

### Ejecutar tests por marcador

```bash
# Solo tests de preprocesamiento
pytest -m preprocessing

# Solo tests del modelo
pytest -m model

# Solo tests de API
pytest -m api
```

### Tests con cobertura

```bash
# Generar reporte de cobertura
pytest --cov=src --cov=api --cov-report=html

# Ver reporte en navegador
# El reporte HTML se genera en htmlcov/index.html
```

### Tests verbose

```bash
# Mostrar información detallada
pytest -v

# Mostrar print statements
pytest -s

# Ambos
pytest -vs
```

### Tests específicos

```bash
# Una clase de tests
pytest tests/test_api.py::TestPredictEndpoint

# Un test específico
pytest tests/test_api.py::TestPredictEndpoint::test_predict_with_valid_data
```

## Requisitos Previos

Antes de ejecutar los tests, asegúrate de que:

1. El modelo entrenado existe en `data/models/`
   - random_forest_model.pkl
   - team_encoder.pkl
   - winner_encoder.pkl

2. Los datos procesados existen en `data/processed/`
   - model_predictions.csv

3. El directorio de src es accesible

## Fixtures y Datos de Prueba

Los tests utilizan fixtures de pytest para crear datos de prueba:

- **sample_raw_data**: Datos sin procesar
- **sample_clean_data**: Datos limpios
- **valid_match_data**: Datos válidos para predicción
- **model_and_encoders**: Modelo y encoders cargados

## Convenciones

- Todos los tests comienzan con `test_`
- Las clases de test comienzan con `Test`
- Los tests están agrupados por funcionalidad
- Cada test tiene un docstring explicativo
- Se usan asserts claros y específicos

## Manejo de Errores

Los tests verifican:
- Validación de entrada
- Manejo de valores nulos
- Manejo de valores extremos
- Errores de tipo de datos
- Errores de la API

## Cobertura Esperada

- **Preprocesamiento**: >90%
- **Modelo**: >85%
- **API**: >80%
- **General**: >85%

## Mejora Continua

Para añadir nuevos tests:

1. Seguir la estructura existente
2. Usar fixtures cuando sea apropiado
3. Escribir tests claros y específicos
4. Documentar con docstrings
5. Verificar cobertura

## Integración Continua

Estos tests están diseñados para ejecutarse en pipelines de CI/CD:

```yaml
# Ejemplo para GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    pytest --cov --cov-report=xml
```

## Troubleshooting

### Problema: ModuleNotFoundError
**Solución**: Verificar que el PYTHONPATH incluya los directorios src y api

### Problema: Archivos no encontrados
**Solución**: Ejecutar tests desde el directorio raíz del proyecto

### Problema: Tests de API fallan
**Solución**: Verificar que los archivos del modelo existan en data/models/

## Contacto

Para dudas o mejoras, contactar al equipo de desarrollo.
