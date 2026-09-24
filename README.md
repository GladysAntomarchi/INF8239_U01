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

---

## LAB03 — Ensambles, reducción dimensional y Green AI

LAB03 amplía el problema desarrollado en LAB02 utilizando el mismo dataset, target, variables predictoras y partición de entrenamiento y prueba.

### Protocolo congelado

- **Dataset:** Online Shoppers Purchasing Intention
- **Target:** `Revenue`
- **Métrica principal:** F1-macro
- **Clase prioritaria:** `Revenue=True`
- **Registros después de eliminar duplicados:** 12,205
- **Entrenamiento:** 9,764 observaciones
- **Prueba:** 2,441 observaciones
- **Split:** 80 % / 20 %, estratificado
- **Random state:** 42

La partición definida en LAB02 se mantuvo sin modificaciones para todas las comparaciones.

### Modelos comparados

Se evaluaron seis configuraciones:

- Regresión logística.
- SVM con `C=1`.
- SVM con `C=10`.
- Random Forest con 100 árboles.
- Random Forest con 300 árboles.
- HistGradientBoostingClassifier.

Cada configuración fue entrenada tres veces y se utilizó la mediana del tiempo de ajuste.

### Resultados Green AI

| Modelo | F1-macro | Recall Revenue=True | Mediana ajuste (s) | Inferencia (ms) | Tamaño (KB) | Pareto |
|---|---:|---:|---:|---:|---:|---|
| boost | 0.8006 | 0.6126 | 0.2443 | 13.3632 | 333.5488 | Sí |
| logistic | 0.7347 | 0.4136 | 0.0837 | 6.8037 | 6.7441 | Sí |
| svm_c1 | 0.7740 | 0.5183 | 6.3510 | 418.6143 | 1681.6152 | No |
| svm_c10 | 0.7688 | 0.5393 | 7.6617 | 429.1537 | 1771.8809 | No |
| rf_100 | 0.7121 | 0.3377 | 0.1529 | 31.8306 | 2065.0732 | No |
| rf_300 | 0.7116 | 0.3377 | 0.3880 | 53.8300 | 6169.6045 | No |

Los resultados completos se almacenan en:

`reports/green_ai_results.csv`

### PCA

PCA se aplicó únicamente al bloque de 10 variables numéricas.

Se seleccionaron 8 componentes para conservar aproximadamente 97.84 % de la varianza.

- SVM sin PCA: F1-macro = 0.7740
- SVM con PCA: F1-macro = 0.7734

La reducción dimensional produjo una diferencia absoluta de apenas 0.0006 en F1-macro.

### t-SNE

Se generaron dos visualizaciones con semillas diferentes:

`reports/tsne_two_seeds.png`

También se evaluó la sensibilidad a `perplexity` utilizando los valores 5, 15, 30 y 50:

`reports/tsne_perplexity_comparison.png`

Las visualizaciones muestran algunos patrones relativamente estables, aunque las clases continúan parcialmente mezcladas. Las formas y distancias de t-SNE no se interpretan como evidencia de grupos reales ni como validación del clasificador.

### Frontera de Pareto

La frontera de Pareto quedó formada por:

- `boost`
- `logistic`

La comparación entre estas dos alternativas mostró:

- Diferencia absoluta de F1-macro: **0.0659**
- Ahorro temporal de `logistic` frente a `boost`: **65.75 %**
- Diferencia de tamaño: **326.8 KB**
- Reducción relativa de tamaño con `logistic`: **97.98 %**
- Ahorro de inferencia con `logistic`: **49.09 %**

Considerando que F1-macro fue definida previamente como la métrica principal y `Revenue=True` como la clase prioritaria, `boost` se seleccionó como la alternativa principal del experimento.

La figura correspondiente se encuentra en:

`reports/pareto.png`

### Modelos serializados

Los modelos entrenados se generan localmente en:

`reports/models/`

Los archivos `.joblib` no se versionan en Git debido a la configuración de `.gitignore`, pero pueden reproducirse ejecutando el notebook de LAB03.

### Entorno de medición

- Python: 3.14.2
- Sistema operativo: Windows 11
- Procesador: Intel64 Family 6 Model 154 Stepping 3, GenuineIntel
- scikit-learn: 1.9.1

Los tiempos representan mediciones contextuales realizadas en este entorno y no deben interpretarse como consumo energético o emisiones de carbono exactas.

### Pruebas

La función de Pareto se implementó en:

`src/inf8239_u01/green.py`

y sus pruebas en:

`tests/test_green.py`

Resultado actual del proyecto:

`10 passed, 1 warning`

La advertencia corresponde al uso de `SVC(probability=True)` en versiones actuales de scikit-learn.

