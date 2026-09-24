# INF8239_U01

Proyecto reproducible de la **Unidad 01 de INF-8239 Ciencia de Datos II**.

El repositorio integra preparación del entorno, experimentación con SVM, selección y auditoría de un dataset público, comparación de modelos, reducción dimensional y análisis de eficiencia computacional bajo un enfoque Green AI.

---

## Ejercicios evaluados

- **Ejercicio 01:** Dataset público y SVM reproducible.
- **Ejercicio 02:** Ensambles, reducción dimensional y Green AI.

---

## Estructura del proyecto

```text
INF8239_U01/
├── data/             # Datos descargados localmente
├── docs/             # Documentación y ficha del dataset
├── notebooks/        # Desarrollo experimental
├── reports/          # Métricas, CSV, figuras y modelos
│   └── models/
├── src/              # Código reutilizable
├── tests/            # Pruebas automatizadas
├── requirements.txt
└── README.md
```

- `data/`: datos descargados localmente.
- `docs/`: documentación y ficha del dataset.
- `notebooks/`: desarrollo experimental.
- `reports/`: métricas, CSV, figuras y modelos.
- `src/`: código reutilizable.
- `tests/`: pruebas automatizadas.


---

## Entorno utilizado

- **Sistema operativo:** Windows 11
- **Python:** 3.14.2
- **scikit-learn:** 1.9.1
- **Git:** 2.55.0.windows.5
- **Editor:** Visual Studio Code
- **Entorno virtual:** `.venv`

---

## Creación y activación del entorno virtual

Desde PowerShell:

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

---

## Orden recomendado de ejecución

Para reproducir el proyecto completo, ejecutar los notebooks en el siguiente orden:

1. `notebooks/00_verificacion.ipynb`
2. `notebooks/01_svm_guiada.ipynb`
3. `notebooks/02_dataset_audit.ipynb`
4. `notebooks/03_online_shoppers_audit.ipynb`
5. `notebooks/04_green_ai_experiments.ipynb`

---

# LAB01 — SVM con pipeline y validación cruzada

Se desarrolló una línea base mediante `DummyClassifier` y una SVM con kernel RBF dentro de un `Pipeline` con `StandardScaler`, utilizando el dataset **Breast Cancer Wisconsin Diagnostic** con una partición estratificada 80/20.

## Resultados principales

| Modelo / etapa | F1-macro |
|---|---:|
| DummyClassifier | 0.3871 |
| SVM base | 0.9812 |
| Mejor GridSearchCV | 0.9812 en prueba |

**Mejor configuración obtenida mediante GridSearchCV:**

- `C = 10`
- `gamma = 0.01`

**F1-macro promedio de validación cruzada:** 0.9739

La configuración ajustada produjo las mismas 114 predicciones que la SVM base sobre el conjunto de prueba, por lo que la mejora observada durante la validación cruzada no se tradujo en una mejora adicional de las métricas finales para esta partición.

**Resultados de validación guardados en:**

`reports/svm_cv_results.csv`

El modelo seleccionado se genera localmente en:

`reports/svm_best.joblib`

---

# Ejercicio 01 — Dataset público y SVM reproducible

## Dataset

**Online Shoppers Purchasing Intention**

- **Fuente:** UCI Machine Learning Repository
- **Target:** `Revenue`
- **Unidad de análisis:** sesión de navegación
- **Licencia:** CC BY 4.0
- **Registros originales:** 12,330
- **Variables:** 18

**Ficha oficial:**

[UCI Machine Learning Repository - Online Shoppers Purchasing Intention](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)

La ficha comparativa de datasets y la documentación de la selección se encuentran en:

`docs/ficha_dataset.md`

## Descarga reproducible

La descarga se implementó en:

`src/inf8239_u01/data.py`

Desde la raíz del proyecto:

```powershell
$env:PYTHONPATH="src"
python -c "from inf8239_u01.data import download_online_shoppers; print(download_online_shoppers())"
```

El dataset se almacena localmente en:

`data/raw/online_shoppers_intention.csv`

Los datos originales no se versionan en Git.

## Auditoría y preparación del dataset

Durante el tamizaje se identificaron:

- **125 duplicados exactos**, que fueron eliminados.
- **0 valores ausentes**.
- **17 variables predictoras**:
  - 10 variables numéricas.
  - 7 variables categóricas.
- **1 variable objetivo:** `Revenue`.

Después de eliminar los duplicados quedaron **12,205 observaciones**.

### Distribución del target

- `Revenue=False`: 84.37 %
- `Revenue=True`: 15.63 %

Debido al desbalance de clases, se utilizó **F1-macro** como métrica principal.

## Preprocesamiento

El preprocesamiento se implementó mediante `ColumnTransformer`:

- Variables numéricas:
  - imputación por mediana;
  - `StandardScaler`.
- Variables categóricas:
  - imputación por moda;
  - `OneHotEncoder(handle_unknown="ignore")`.

Las transformaciones se ajustan exclusivamente utilizando los datos de entrenamiento para prevenir fuga de información.

La variable objetivo `Revenue` se excluye completamente del conjunto de predictores `X`.

`PageValues` se documentó como variable de atención por su posible riesgo temporal o informativo, sin considerarse automáticamente como fuga confirmada.

## Resultados del modelo

| Modelo | Accuracy | F1-macro | Precision Revenue=True | Recall Revenue=True |
|---|---:|---:|---:|---:|
| DummyClassifier | 0.8435 | 0.4576 | 0.0000 | 0.0000 |
| SVM RBF Base | 0.8955 | 0.7740 | 0.7361 | 0.5183 |

El `DummyClassifier` alcanzó una accuracy elevada debido al desbalance de clases, pero no identificó ninguna observación `Revenue=True`.

La SVM RBF base mejoró sustancialmente el F1-macro y logró identificar parte de las sesiones que finalizaron en compra, aunque el recall de 0.5183 muestra que todavía existe margen de mejora.

## Artefactos del Ejercicio 01

**Resultados tabulares:**

`reports/lab02_model_results.csv`

**Figuras:**

- `reports/revenue_distribution.png`
- `reports/svm_confusion_matrix.png`

---
# Ejercicio 02 — Ensambles, reducción y Green AI

Se mantuvieron el mismo dataset, target, variables predictoras y partición definidos en el Ejercicio 01.

## Protocolo experimental

- **Registros totales:** 12,205
- **Conjunto de entrenamiento:** 9,764 observaciones
- **Conjunto de prueba:** 2,441 observaciones
- **Partición:** 80 % entrenamiento / 20 % prueba, estratificada
- **Random state:** 42
- **Métrica principal:** F1-macro
- **Clase prioritaria:** `Revenue=True`

Para garantizar una comparación homogénea, todas las configuraciones utilizaron la misma partición y el mismo esquema de preprocesamiento.

Cada modelo fue ajustado **tres veces**. Para comparar el costo computacional se registraron:

- mediana del tiempo de entrenamiento;
- tiempo de inferencia;
- tamaño serializado del modelo.

## Modelos comparados

Se evaluaron seis configuraciones:

1. Logistic Regression.
2. SVM con `C=1`.
3. SVM con `C=10`.
4. Random Forest con 100 árboles.
5. Random Forest con 300 árboles.
6. HistGradientBoosting.

## Resultados principales

| Modelo | F1-macro | Recall Revenue=True | Mediana ajuste (s) | Inferencia (ms) | Tamaño (KB) | Pareto |
|---|---:|---:|---:|---:|---:|---|
| boost | 0.8006 | 0.6126 | 0.2443 | 13.3632 | 333.5488 | Sí |
| logistic | 0.7347 | 0.4136 | 0.0837 | 6.8037 | 6.7441 | Sí |
| svm_c1 | 0.7740 | 0.5183 | 6.3510 | 418.6143 | 1681.6152 | No |
| svm_c10 | 0.7688 | 0.5393 | 7.6617 | 429.1537 | 1771.8809 | No |
| rf_100 | 0.7121 | 0.3377 | 0.1529 | 31.8306 | 2065.0732 | No |
| rf_300 | 0.7116 | 0.3377 | 0.3880 | 53.8300 | 6169.6045 | No |

Los resultados completos se encuentran en:

`reports/green_ai_results.csv`

HistGradientBoosting obtuvo el mayor F1-macro y el mayor recall para la clase prioritaria `Revenue=True`.

Logistic Regression presentó un menor desempeño predictivo, pero fue la configuración más ligera en tiempo de entrenamiento, inferencia y tamaño serializado.

---
## Reducción dimensional y visualización

### PCA

PCA se aplicó únicamente al bloque de **10 variables numéricas**.

Se seleccionaron **8 componentes principales**, conservando aproximadamente **97.84 % de la varianza acumulada**.

| Configuración | F1-macro |
|---|---:|
| SVM sin PCA | 0.7740 |
| SVM con PCA | 0.7734 |

La diferencia absoluta fue de apenas **0.0006 en F1-macro**, por lo que la reducción dimensional prácticamente no modificó el desempeño predictivo de la SVM.

**Figura:**

`reports/pca_cumulative_variance.png`

### t-SNE

Se realizaron dos análisis exploratorios:

1. Comparación con `perplexity=30` utilizando las semillas 42 y 7.
2. Sensibilidad al hiperparámetro `perplexity` utilizando los valores 5, 15, 30 y 50.

**Figuras:**

- `reports/tsne_two_seeds.png`
- `reports/tsne_perplexity_comparison.png`

Las representaciones mostraron cierta estabilidad general ante cambios de semilla y sensibilidad al valor de `perplexity`.

Las clases permanecieron parcialmente solapadas, por lo que t-SNE se interpreta únicamente con fines exploratorios. Las formas, distancias y agrupaciones observadas no se consideran evidencia directa de separación real de clases ni validación del clasificador.

---
## Green AI y frontera de Pareto

La frontera de Pareto quedó conformada por:

- `boost` — HistGradientBoosting.
- `logistic` — Logistic Regression.

La comparación entre ambas alternativas mostró:

- **Ahorro en tiempo de entrenamiento con Logistic Regression:** 65.75 %
- **Reducción relativa del tamaño del modelo:** 97.98 %
- **Ahorro en tiempo de inferencia:** 49.09 %
- **Diferencia absoluta de F1-macro:** 0.0659

HistGradientBoosting obtuvo el mayor F1-macro y el mayor recall para la clase prioritaria `Revenue=True`.

Logistic Regression presentó un menor desempeño predictivo, pero un costo computacional considerablemente inferior.

Debido a que F1-macro fue definida previamente como la métrica principal y `Revenue=True` como la clase prioritaria, **HistGradientBoosting** se seleccionó como la alternativa principal del experimento.

**Figura:**

`reports/pareto.png`

Los tiempos reportados representan mediciones contextuales realizadas en el entorno utilizado y no deben interpretarse como mediciones directas de consumo energético o emisiones de carbono.

---

## Modelos serializados

Los seis modelos evaluados en el Ejercicio 02 fueron serializados mediante `joblib` y se encuentran versionados en:

`reports/models/`

Se incluyen:

- `boost.joblib`
- `logistic.joblib`
- `rf_100.joblib`
- `rf_300.joblib`
- `svm_c1.joblib`
- `svm_c10.joblib`

---
## Pruebas automatizadas

Para ejecutar la suite de pruebas desde la raíz del proyecto:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

### Resultado actual

`10 passed, 1 warning`

La advertencia corresponde al uso de `SVC(probability=True)` en la versión actual de scikit-learn y no representa una falla de las pruebas.

### Cobertura de pruebas

Las pruebas automatizadas incluyen:

- validación básica del entorno;
- contrato del dataset: existencia, tamaño mínimo, columnas esperadas, target sin valores ausentes y presencia de al menos dos clases;
- construcción y validaciones básicas de los modelos;
- comportamiento de la función de frontera de Pareto.

---

## Artefactos principales

### Archivos CSV

- `reports/svm_cv_results.csv`
- `reports/lab02_model_results.csv`
- `reports/green_ai_results.csv`

### Figuras

- `reports/revenue_distribution.png`
- `reports/svm_confusion_matrix.png`
- `reports/pca_cumulative_variance.png`
- `reports/tsne_two_seeds.png`
- `reports/tsne_perplexity_comparison.png`
- `reports/pareto.png`

### Modelos serializados

- `reports/models/boost.joblib`
- `reports/models/logistic.joblib`
- `reports/models/rf_100.joblib`
- `reports/models/rf_300.joblib`
- `reports/models/svm_c1.joblib`
- `reports/models/svm_c10.joblib`

---

## Reproducibilidad

El proyecto garantiza la reproducibilidad mediante:

- entorno virtual independiente;
- dependencias definidas en `requirements.txt`;
- semillas reproducibles;
- partición estratificada;
- uso de `Pipeline` y `ColumnTransformer`;
- código reutilizable en `src/`;
- pruebas automatizadas con `pytest`;
- resultados, figuras y modelos almacenados en `reports/`;
- control de versiones mediante Git.

Los datos originales se descargan de forma reproducible y no se almacenan directamente en el repositorio.

---
