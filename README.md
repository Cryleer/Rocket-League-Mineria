# 🚀 Rocket League - Sistema de Predicción ML

Sistema completo de Machine Learning para predecir ganadores de partidas de Rocket League con **97% de precisión**.

[![Tests](https://img.shields.io/badge/tests-82%2F82%20passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-57%25-yellow)](htmlcov/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Demo Rápida](#-demo-rápida)
- [Arquitectura](#️-arquitectura)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Tests](#-tests)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación](#-documentación)
- [Resultados](#-resultados)

---

## ✨ Características

### 🤖 Machine Learning
- **Modelo**: Random Forest Classifier
- **Accuracy**: 97%
- **Features**: 8 características optimizadas
- **Datos**: 500 partidas analizadas

### 🌐 API REST (FastAPI)
- 3 endpoints funcionales
- Documentación automática (Swagger)
- Validación de datos con Pydantic
- Generación de datos sintéticos

### 📊 Dashboard Interactivo (Dash/Plotly)
- Visualizaciones en tiempo real
- Filtros por modo de juego
- Generación de predicciones on-demand
- 4 KPIs + 3 gráficos interactivos

### ✅ Testing Completo
- 82 tests unitarios (100% passing)
- Coverage: 57% en API
- Tests automatizados con pytest
- CI/CD ready

---

## 🎬 Demo Rápida

### Inicio en 30 segundos

```powershell
# 1. Clonar/Descargar proyecto
cd "H:\Rocket Mineria"

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar sistema completo
.\iniciar.bat
```

**Acceder a:**
- 🌐 API: http://localhost:8000/docs
- 📊 Dashboard: http://localhost:8050

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                   USUARIO                               │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
   ┌────▼────┐      ┌────▼────┐
   │   API   │      │Dashboard│
   │FastAPI  │      │  Dash   │
   │:8000    │      │  :8050  │
   └────┬────┘      └────┬────┘
        │                │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Modelo ML      │
        │ Random Forest   │
        │  97% accuracy   │
        └─────────────────┘
```

### Tecnologías

| Componente | Tecnología |
|------------|------------|
| **Backend** | FastAPI 0.104+ |
| **Frontend** | Dash 3.3+, Plotly |
| **ML** | scikit-learn 1.4+ |
| **Testing** | pytest 9.0+, pytest-cov |
| **Data** | pandas 2.2+, numpy 1.26+ |

---

## 📦 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip actualizado
- 500 MB espacio en disco

### Instalación Completa

```powershell
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/rocket-mineria.git
cd rocket-mineria

# 2. Crear entorno virtual (opcional)
python -m venv .venv
.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Instalar dependencias de testing
pip install -r requirements-test.txt

# 5. Entrenar modelo (si no existe)
python src\cleaning.py
python src\features.py
python src\encode_and_pipeline.py
python src\train_model.py

# 6. Generar predicciones
python src\generate_predictions_with_winner.py
```

---

## 🎮 Uso

### Opción 1: Inicio Automático (Recomendado)

```powershell
.\iniciar.bat
```

Esto iniciará:
- ✅ API en puerto 8000
- ✅ Dashboard en puerto 8050
- ✅ Navegadores automáticamente

### Opción 2: Inicio Manual

**Terminal 1 - API:**
```powershell
python api\main.py
```

**Terminal 2 - Dashboard:**
```powershell
python dashboard\app.py
```

**Terminal 3 - Tests:**
```powershell
python run_tests.py all
```

---

## 🔌 API Endpoints

### 1. Root - Información del API

```http
GET http://localhost:8000/
```

**Respuesta:**
```json
{
  "status": "active",
  "message": "Rocket League Winner Prediction API v2.6",
  "endpoints": {
    "predict": "/predict",
    "generate_synthetic": "/generate_synthetic",
    "stats": "/stats"
  },
  "encoders": {
    "team_color_classes": ["Blue", "Orange"],
    "winner_classes": ["Blue", "Draw", "Orange"]
  }
}
```

### 2. Predict - Predecir Ganador

```http
POST http://localhost:8000/predict
Content-Type: application/json
```

**Request:**
```json
{
  "team_color": "Blue",
  "game_mode": "Standard",
  "goal_difference": 3,
  "match_duration": 300,
  "overtime": false,
  "is_competitive": 1
}
```

**Response:**
```json
{
  "winner_prediction": "Blue",
  "confidence": 0.95,
  "probabilities": {
    "Blue": 0.95,
    "Orange": 0.03,
    "Draw": 0.02
  }
}
```

### 3. Generate Synthetic - Generar Partidas

```http
POST http://localhost:8000/generate_synthetic
Content-Type: application/json
```

**Request:**
```json
{
  "n_matches": 100,
  "game_mode": "Duel"
}
```

**Response:**
```json
{
  "status": "success",
  "summary": {
    "total_matches": 100,
    "predictions": {
      "orange": 45,
      "blue": 42,
      "draw": 13
    },
    "avg_confidence": 0.87
  }
}
```

### 4. Stats - Estadísticas

```http
GET http://localhost:8000/stats
```

**Response:**
```json
{
  "total_matches": 500,
  "game_modes": {
    "Standard": 178,
    "Doubles": 171,
    "Duel": 151
  },
  "predicted_winner_distribution": {
    "orange": 237,
    "blue": 231,
    "draw": 32
  },
  "avg_match_duration": 320.5,
  "overtime_percentage": 18.4
}
```

---

## ✅ Tests

### Ejecutar Todos los Tests

```powershell
python run_tests.py all
```

**Resultado:**
```
82/82 tests PASSED ✅
Coverage: 57%
Time: ~3 seconds
```

### Ejecutar Tests Específicos

```powershell
# Solo tests de API
pytest tests/test_api.py -v

# Solo tests de modelo
pytest tests/test_model.py -v

# Solo tests de preprocesamiento
pytest tests/test_preprocessing.py -v
```

### Ver Cobertura

```powershell
python run_tests.py coverage
```

Esto generará un reporte HTML en `htmlcov/index.html`

### Estadísticas de Tests

| Módulo | Tests | Estado |
|--------|-------|--------|
| **API** | 32 | ✅ 100% |
| **Modelo** | 31 | ✅ 100% |
| **Preprocesamiento** | 19 | ✅ 100% |
| **TOTAL** | **82** | ✅ **100%** |

---

## 📁 Estructura del Proyecto

```
Rocket Mineria/
│
├── 📄 README.md                    # Este archivo
├── 📄 INICIO_RAPIDO.md             # Guía rápida 5 min
├── 📄 RESUMEN_TESTS.md             # Resumen ejecutivo
├── 📄 INDICE.md                    # Índice de entrega
│
├── 🚀 iniciar.bat                  # Script de inicio automático
├── ⚙️  pytest.ini                   # Configuración pytest
├── 🐍 run_tests.py                 # Script de tests
├── 📋 requirements.txt             # Dependencias principales
├── 📋 requirements-test.txt        # Dependencias de testing
│
├── 📁 api/                         # API REST FastAPI
│   └── main.py                     # Endpoints y lógica API
│
├── 📁 dashboard/                   # Dashboard interactivo
│   └── app.py                      # Interfaz Dash/Plotly
│
├── 📁 src/                         # Código fuente ML
│   ├── cleaning.py                 # Limpieza de datos
│   ├── features.py                 # Ingeniería de features
│   ├── encode_and_pipeline.py      # Codificación
│   ├── train_model.py              # Entrenamiento
│   ├── batch_predictions.py        # Predicciones batch
│   └── generate_predictions_with_winner.py  # Gen. con winner
│
├── 📁 tests/                       # Tests unitarios
│   ├── README.md                   # Documentación tests
│   ├── test_api.py                 # 32 tests API
│   ├── test_model.py               # 31 tests modelo
│   └── test_preprocessing.py       # 19 tests preprocesamiento
│
├── 📁 data/                        # Datos y modelos
│   ├── models/                     # Modelos entrenados
│   │   ├── random_forest_model.pkl # Modelo principal (97%)
│   │   ├── team_encoder.pkl        # Encoder equipos
│   │   └── winner_encoder.pkl      # Encoder ganadores
│   │
│   └── processed/                  # Datos procesados
│       ├── model_predictions.csv   # Predicciones con winner
│       ├── synthetic_predictions.csv  # Predicciones sintéticas
│       └── processed_encoded.csv   # Datos codificados
│
└── 📁 docs/                        # Documentación adicional
    └── pruebas/
        └── EVIDENCIAS_PRUEBAS.md   # Evidencias formales
```

---

## 📚 Documentación

### Documentos Disponibles

1. **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Guía de inicio en 5 minutos
2. **[RESUMEN_TESTS.md](RESUMEN_TESTS.md)** - Resumen ejecutivo completo
3. **[INDICE.md](INDICE.md)** - Índice de archivos entregados
4. **[tests/README.md](tests/README.md)** - Documentación técnica de tests
5. **[docs/pruebas/EVIDENCIAS_PRUEBAS.md](docs/pruebas/EVIDENCIAS_PRUEBAS.md)** - Evidencias formales

### API Documentation

La documentación interactiva de la API está disponible en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📊 Resultados

### Métricas del Modelo

| Métrica | Valor |
|---------|-------|
| **Accuracy** | 97.0% |
| **F1 Score (Macro)** | 91.2% |
| **Precision** | 96.8% |
| **Recall** | 96.5% |
| **Total Predicciones** | 500 |

### Distribución de Predicciones

```
Orange:  237 (47.4%)
Blue:    231 (46.2%)
Draw:     32 (6.4%)
```

### Performance

| Componente | Métrica | Valor |
|------------|---------|-------|
| **API** | Latencia | ~50ms |
| **Modelo** | Inferencia | ~5ms |
| **Dashboard** | Carga | ~2s |
| **Tests** | Ejecución | ~3s |

---

## 🎓 Para Profesores/Evaluadores

### Verificación Rápida

```powershell
# 1. Clonar/descomprimir
cd "Rocket Mineria"

# 2. Instalar
pip install -r requirements.txt
pip install -r requirements-test.txt

# 3. Ejecutar tests
python run_tests.py all

# Resultado esperado: 82/82 PASSED ✅
```

### Archivos Clave para Evaluación

1. **Tests**: `tests/test_*.py` (82 tests, 100% passing)
2. **Evidencias**: `docs/pruebas/EVIDENCIAS_PRUEBAS.md`
3. **Código ML**: `src/train_model.py` (97% accuracy)
4. **API**: `api/main.py` (3 endpoints funcionales)
5. **Dashboard**: `dashboard/app.py` (interfaz interactiva)

### Puntos Destacados

✅ **97 accuracy del modelo**  
✅ **82 tests unitarios (100% passing)**  
✅ **Documentación profesional completa**  
✅ **Sistema end-to-end funcional**  
✅ **API REST con Swagger docs**  
✅ **Dashboard interactivo en tiempo real**  
✅ **Scripts de automatización**  
✅ **Cobertura de código**  

---

## 🛠️ Desarrollo

### Comandos Útiles

```powershell
# Entrenar modelo desde cero
python src\train_model.py

# Generar predicciones
python src\generate_predictions_with_winner.py

# Ejecutar tests con verbose
pytest tests/ -v

# Ver cobertura detallada
pytest tests/ --cov=api --cov=src --cov-report=html

# Limpiar archivos temporales
Remove-Item -Recurse -Force __pycache__, .pytest_cache, htmlcov
```

### Agregar Nuevos Tests

1. Crear archivo en `tests/test_nuevo.py`
2. Importar fixtures necesarias
3. Seguir convención de nombres: `test_descripcion`
4. Ejecutar: `pytest tests/test_nuevo.py -v`

---

## 🚀 Despliegue

### Despliegue Local

Ya está listo para despliegue local con `iniciar.bat`

### Despliegue en Servidor

```bash
# API
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Dashboard
gunicorn dashboard.app:server --bind 0.0.0.0:8050
```

### Docker (Futuro)

```dockerfile
# TODO: Agregar Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
```

---

## 🤝 Contribuir

### Guidelines

1. Fork el proyecto
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Add: nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Estándares de Código

- **Python**: PEP 8
- **Tests**: Coverage mínimo 80%
- **Commits**: Conventional Commits
- **Documentación**: Docstrings en todas las funciones

---

## 📝 Changelog

### v1.0.0 

#### Added
- ✨ Sistema completo de ML para Rocket League
- ✨ API REST con FastAPI (3 endpoints)
- ✨ Dashboard interactivo con Dash/Plotly
- ✨ 82 tests unitarios (100% passing)
- ✨ Documentación completa
- ✨ Script de inicio automático

#### Model
- 🤖 Random Forest Classifier (97% accuracy)
- 🤖 8 features optimizadas
- 🤖 3 encoders (team, winner, mode)

#### Documentation
- 📚 README.md principal
- 📚 INICIO_RAPIDO.md
- 📚 RESUMEN_TESTS.md
- 📚 EVIDENCIAS_PRUEBAS.md


---

## 🙏 Agradecimientos

- **scikit-learn**: Framework de Machine Learning
- **FastAPI**: Framework web moderno y rápido
- **Dash/Plotly**: Visualizaciones interactivas
- **pytest**: Framework de testing
- **Pandas**: Manipulación de datos

---

## 🎯 Roadmap

### v1.1 (Futuro)
- [ ] Agregar más algoritmos ML (XGBoost, Neural Networks)
- [ ] Sistema de autenticación en API
- [ ] Base de datos PostgreSQL
- [ ] Deploy en cloud (AWS/Azure)
- [ ] CI/CD con GitHub Actions
- [ ] Containerización con Docker
- [ ] Más visualizaciones en dashboard
- [ ] Exportar reportes PDF

### v2.0 (Futuro)
- [ ] Predicción en tiempo real (streaming)
- [ ] Integración con Rocket League API oficial
- [ ] Sistema de recomendaciones
- [ ] Mobile app (React Native)
- [ ] Multi-tenancy
- [ ] A/B testing de modelos

---

</div>
