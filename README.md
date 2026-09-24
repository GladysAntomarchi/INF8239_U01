# INF8239_U01

Laboratorio de preparación y validación del entorno profesional para la asignatura INF-8239.

## Entorno utilizado

- Sistema operativo: Windows 11
- Python: 3.14.2
- Git: 2.55.0.windows.5
- Editor: Visual Studio Code
- Entorno virtual: `.venv`

## Estructura del proyecto

- `data/`: datos del proyecto.
- `docs/`: documentación y ficha del dataset.
- `notebooks/`: notebooks de Jupyter.
- `reports/`: reportes y resultados.
- `src/`: código fuente.
- `tests/`: pruebas unitarias.

## Creación y activación del entorno virtual

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.venv\Scripts\Activate.ps1
```

## Instalación de dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecución de pruebas

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

### Resultado actual

`8 passed, 1 warning`

La advertencia corresponde a la depreciación futura del parámetro `probability=True` utilizado en el SVC del LAB01.

---

## LAB01 — SVM con pipeline y validación cruzada

Se construyó una línea base mediante `DummyClassifier` y una SVM con kernel RBF dentro de un `Pipeline` con `StandardScaler`, evitando ajustar el escalado antes de separar entrenamiento y prueba.

### Resultados principales

- Dataset: Breast Cancer Wisconsin Diagnostic.
- Observaciones: 569.
- Predictores: 30.
- Partición: 80 % entrenamiento y 20 % prueba, estratificada.
- F1-macro baseline: 0.3871.
- F1-macro SVM base en prueba: 0.9812.
- ROC-AUC SVM base: 0.9950.
- Mejor configuración de GridSearchCV:
  - C = 10
  - gamma = 0.01
- F1-macro promedio de validación cruzada: 0.9739.
- F1-macro del modelo seleccionado en prueba: 0.9812.

La configuración ajustada produjo las mismas 114 predicciones que la SVM base sobre el conjunto de prueba, por lo que la mejora observada durante la validación cruzada no se tradujo en una mejora de las métricas finales para esta partición.

Los resultados de la búsqueda se guardan en `reports/svm_cv_results.csv`. El modelo serializado se genera localmente en `reports/svm_best.joblib`.

---

## LAB02 — Dataset público: Online Shoppers Purchasing Intention

### Problema

Se plantea un problema de clasificación binaria orientado a predecir si una sesión de navegación en un sitio de comercio electrónico finalizará en una compra.

- **Dataset:** Online Shoppers Purchasing Intention
- **Fuente:** UCI Machine Learning Repository
- **Target:** `Revenue`
- **Unidad de análisis:** sesión de navegación
- **Métrica principal:** F1-macro
- **Split:** 80 % entrenamiento / 20 % prueba
- **Estratificación:** sí
- **Random state:** 42

### Fuente y licencia

El dataset se obtiene desde el UCI Machine Learning Repository y está disponible bajo licencia CC BY 4.0.

Ficha del dataset:

https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset

La descarga reproducible se implementó en:

`src/inf8239_u01/data.py`

El archivo descargado se almacena localmente en:

`data/raw/online_shoppers_intention.csv`

Los datos originales no se versionan en Git.

### Descarga reproducible

Desde la raíz del proyecto:

```powershell
$env:PYTHONPATH="src"
python -c "from inf8239_u01.data import download_online_shoppers; print(download_online_shoppers())"
```

### Auditoría del dataset

El dataset original contiene 12,330 registros y 18 columnas.

Durante el tamizaje se identificaron:

- 125 registros duplicados exactos.
- 0 valores ausentes.
- 17 variables predictoras.
- 1 variable objetivo: `Revenue`.

Los duplicados exactos fueron eliminados mediante código antes de realizar la partición, quedando 12,205 observaciones.

La distribución del target después de la limpieza fue:

- `Revenue=False`: 84.37 %
- `Revenue=True`: 15.63 %

Debido al desbalance, se utiliza F1-macro como métrica principal.

### Preprocesamiento

Se identificaron 10 variables numéricas y 7 categóricas.

El preprocesamiento se implementó mediante `ColumnTransformer`:

- Variables numéricas: imputación por mediana y `StandardScaler`.
- Variables categóricas: imputación por moda y `OneHotEncoder`.
- `handle_unknown="ignore"` para categorías no observadas durante el entrenamiento.

Las transformaciones se ajustan únicamente con los datos de entrenamiento para prevenir fuga de información.

### Resultados iniciales

| Modelo | Accuracy | F1-macro | Precision Revenue=True | Recall Revenue=True |
|---|---:|---:|---:|---:|
| DummyClassifier | 0.8435 | 0.4576 | 0.0000 | 0.0000 |
| SVM RBF Base | 0.8955 | 0.7740 | 0.7361 | 0.5183 |

El `DummyClassifier` obtiene una accuracy elevada debido al desbalance, pero no identifica ninguna sesión que finalice en compra.

La SVM base mejora sustancialmente el F1-macro y logra identificar parte de las sesiones con `Revenue=True`, aunque el recall de 0.5183 muestra que todavía existe margen de mejora.

Los resultados fueron guardados en:

`reports/lab02_model_results.csv`

### Riesgo de fuga

No se identificó una variable equivalente directamente al target dentro de los predictores.

`PageValues` se mantiene inicialmente como predictor, pero se documentó como variable de atención debido a su relación con el comportamiento previo a una transacción. En experimentos posteriores podrá evaluarse el desempeño del modelo con y sin esta característica.

### Pruebas

El contrato de datos se encuentra en:

`tests/test_data_contract.py`

Para ejecutar todas las pruebas:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

Resultado actual:

`8 passed, 1 warning`

La advertencia corresponde a la depreciación futura del parámetro `probability=True` utilizado en el SVC del LAB01.

