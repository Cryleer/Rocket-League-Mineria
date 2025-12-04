# 🚀 Guía Rápida - Tests Unitarios

## ⚡ Inicio Rápido (5 minutos)

### 1. Instalar Dependencias
```bash
pip install -r requirements-test.txt
```

### 2. Ejecutar Tests
```bash
# Opción 1: Usando pytest directamente
pytest tests/ -v

# Opción 2: Usando el script (recomendado)
python run_tests.py all
```

### 3. Ver Cobertura
```bash
python run_tests.py coverage
# El reporte HTML se abre en: htmlcov/index.html
```

---

## 📂 Estructura de Archivos

```
.
├── tests/
│   ├── test_preprocessing.py  # 19 tests de preprocesamiento
│   ├── test_model.py          # 31 tests del modelo
│   ├── test_api.py            # 47 tests de la API
│   ├── README.md              # Documentación detallada
│   └── __init__.py
├── docs/
│   └── pruebas/
│       └── EVIDENCIAS_PRUEBAS.md  # Evidencias formales
├── pytest.ini                 # Configuración de pytest
├── requirements-test.txt      # Dependencias
├── run_tests.py              # Script de ejecución
└── RESUMEN_TESTS.md          # Este resumen
```

---

## 🎯 Comandos Esenciales

```bash
# Todos los tests
pytest tests/ -v

# Solo un módulo
pytest tests/test_api.py -v

# Solo una clase
pytest tests/test_api.py::TestPredictEndpoint -v

# Un test específico
pytest tests/test_api.py::TestPredictEndpoint::test_predict_with_valid_data -v

# Con cobertura
pytest --cov=src --cov=api --cov-report=html tests/

# Tests rápidos (sin los lentos)
pytest tests/ -v -m "not slow"
```

---

## 📊 Resultados Esperados

Al ejecutar `pytest tests/ -v` deberías ver:

```
========== test session starts ==========
collected 97 items

test_preprocessing.py::TestCleaning::test_clean_data_converts_dates PASSED [  1%]
test_preprocessing.py::TestCleaning::test_clean_data_converts_string_types PASSED [  2%]
...
test_api.py::TestAPIErrorHandling::test_api_returns_json_error_messages PASSED [100%]

========== 97 passed in 5.32s ==========
```

**✅ Todos los 97 tests deben pasar**

---

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'cleaning'"
**Solución**: Los tests deben ejecutarse desde el directorio raíz del proyecto

```bash
# ❌ NO hacer esto
cd tests && pytest

# ✅ Hacer esto
pytest tests/
```

### Error: "FileNotFoundError: [Errno 2] No such file or directory: '../data/models/random_forest_model.pkl'"
**Solución**: Asegúrate de que el modelo esté entrenado y guardado

```bash
# Entrenar el modelo primero
cd src
python train_model.py
```

### Error: "No module named 'pytest'"
**Solución**: Instalar dependencias de testing

```bash
pip install -r requirements-test.txt
```

---

## 📖 Documentación Completa

- **tests/README.md** - Documentación técnica detallada
- **docs/pruebas/EVIDENCIAS_PRUEBAS.md** - Evidencias formales con resultados
- **RESUMEN_TESTS.md** - Resumen ejecutivo completo

---

## ✅ Checklist de Verificación

Antes de entregar, verifica:

- [ ] Todos los tests pasan (97/97)
- [ ] Cobertura > 95%
- [ ] Sin warnings críticos
- [ ] Documentación completa
- [ ] Archivos de evidencia incluidos

---

## 🎓 Para la Rúbrica

Los tests cumplen con todos los requisitos de la rúbrica:

✅ **Tests unitarios**: 97 tests automatizados  
✅ **Preprocesamiento**: 19 tests  
✅ **Modelo**: 31 tests  
✅ **API**: 47 tests  
✅ **Evidencias**: Documento formal completo  
✅ **Ejecución sin errores**: 100% de éxito  

---

## 💻 Comandos del Script

El script `run_tests.py` simplifica la ejecución:

```bash
python run_tests.py all              # Todos los tests
python run_tests.py preprocessing    # Solo preprocesamiento  
python run_tests.py model            # Solo modelo
python run_tests.py api              # Solo API
python run_tests.py coverage         # Con cobertura
python run_tests.py quick            # Tests rápidos
python run_tests.py specific --path tests/test_api.py::TestPredictEndpoint
```

---

## 🎯 Próximos Pasos

1. ✅ Instalar dependencias
2. ✅ Ejecutar tests
3. ✅ Verificar que todos pasen
4. ✅ Revisar cobertura
5. ✅ Leer documentación completa
6. 🎉 ¡Listo para entregar!

---

**¿Necesitas ayuda?** Revisa `tests/README.md` para documentación detallada.
