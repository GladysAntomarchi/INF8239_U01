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
├── data/              # Datos descargados localmente
├── docs/              # Documentación y ficha del dataset
├── notebooks/         # Desarrollo experimental
├── reports/           # Métricas, CSV, figuras y modelos
│   └── models/
├── src/               # Código reutilizable
├── tests/             # Pruebas automatizadas
├── requirements.txt
└── README.md

- **`data/`:** Datos descargados localmente.
- **`docs/`:** Documentación y ficha del dataset.
- **`notebooks/`:** Desarrollo experimental.
- **`reports/`:** Métricas, CSV, figuras y modelos.
- **`src/`:** Código reutilizable.
- **`tests/`:** Pruebas automatizadas.

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

## Instalación d edependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Orden recomendado de ejecución

Para reproducir el proyecto completo, ejecuta los notebooks en el siguiente orden secuencial:

1. `notebooks/00_verificacion.ipynb`
2. `notebooks/01_svm_guiada.ipynb`
3. `notebooks/02_dataset_audit.ipynb`
4. `notebooks/03_online_shoppers_audit.ipynb`
5. `notebooks/04_green_ai_experiments.ipynb`

## LAB01 — SVM con pipeline y validación cruzada

Se desarrolló una línea base mediante `DummyClassifier` y una SVM con kernel RBF dentro de un `Pipeline` con `StandardScaler`, utilizando el dataset **Breast Cancer Wisconsin Diagnostic** con una partición estratificada 80/20.

### Resultados principales

| Modelo / etapa | F1-macro |
| :--- | :---: |
| DummyClassifier | 0.3871 |
| SVM base | 0.9812 |
| Mejor GridSearchCV | 0.9812 (en prueba) |

**Mejor configuración obtenida mediante GridSearchCV:**
- `C = 10`
- `gamma = 0.01`

**Resultados de validación guardados en:**
`reports/svm_cv_results.csv`

## Ejercicio 01 — Dataset público y SVM reproducible

### Dataset: Online Shoppers Purchasing Intention

- **Fuente:** UCI Machine Learning Repository
- **Target:** `Revenue`
- **Unidad de análisis:** sesión de navegación
- **Licencia:** CC BY 4.0
- **Registros originales:** 12,330
- **Variables:** 18
- **Ficha oficial:** [UCI Machine Learning Repository - Online Shoppers Purchasing Intention](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)

### Descarga reproducible

La descarga se implementó en:
`src/inf8239_u01/data.py`

Desde la raíz del proyecto (PowerShell):

```powershell
$env:PYTHONPATH="src"
python -c "from inf8239_u01.data import download_online_shoppers; print(download_online_shoppers())"

El dataset se almacena localmente en:
data/raw/online_shoppers_intention.csv
Los datos originales no se versionan en Git.

## Auditoría y preparación del dataset

### Hallazgos iniciales
- **Duplicados exactos:** 125 registros (eliminados; restan 12,205 observaciones).
- **Valores ausentes:** 0.
- **Variables predictoras:** 17 en total.
  - **Variables numéricas:** 10.
  - **Variables categóricas:** 7.

### Distribución del target (`Revenue`)
- `Revenue=False`: 84.37 %
- `Revenue=True`: 15.63 %

### Preprocesamiento (`ColumnTransformer`)
- **Variables numéricas:** imputación por mediana y estandarización con `StandardScaler`.
- **Variables categóricas:** imputación por moda y codificación con `OneHotEncoder` (`handle_unknown="ignore"` para categorías no observadas en entrenamiento).
- Las transformaciones se ajustan exclusivamente sobre los datos de entrenamiento para prevenir fuga de información (*data leakage*).
- La variable objetivo `Revenue` se excluye completamente del conjunto de predictores $X$.
- `PageValues` se documentó como variable de atención debido a su posible riesgo temporal/informativo, sin clasificarse automáticamente como fuga confirmada.

## Resultados del modelo

| Modelo | Accuracy | F1-macro | Precision Revenue=True | Recall Revenue=True |
| :--- | :---: | :---: | :---: | :---: |
| DummyClassifier | 0.8435 | 0.4576 | 0.0000 | 0.0000 |
| SVM RBF Base | 0.8955 | 0.7740 | 0.7361 | 0.5183 |

El baseline evidencia que una accuracy elevada puede resultar engañosa en presencia de desbalance de clases, ya que no detectó ninguna observación con `Revenue=True`.

### Artefactos generados

- **Resultados tabulares:** `reports/lab02_model_results.csv`
- **Figuras:**
  - `reports/revenue_distribution.png`
  - `reports/svm_confusion_matrix.png`

  ## Ejercicio 02 — Ensambles, reducción y Green AI

Se mantuvieron el mismo dataset, target, variables predictoras y partición del Ejercicio 01.

### Protocolo experimental

- **Registros totales:** 12,205
- **Conjunto de entrenamiento:** 9,764
- **Conjunto de prueba:** 2,441
- **Partición:** Split 80/20 estratificado
- **Semilla aleatoria:** `random_state = 42`
- **Métrica principal:** F1-macro
- **Clase prioritaria:** `Revenue=True`

Cada configuración fue entrenada tres veces. Para comparar el costo computacional se registraron:
- Mediana del tiempo de entrenamiento.
- Tiempo de inferencia.
- Tamaño del modelo serializado.

### Modelos comparados

Se evaluaron seis configuraciones:

1. Logistic Regression
2. SVM ($C=1$)
3. SVM ($C=10$)
4. Random Forest (100 árboles)
5. Random Forest (300 árboles)
6. HistGradientBoosting

## Resultados principales

| Modelo | F1-macro | Recall Revenue=True | Mediana ajuste (s) | Inferencia (ms) | Tamaño (KB) | Pareto |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| boost | 0.8006 | 0.6126 | 0.2443 | 13.3632 | 333.5488 | Sí |
| logistic | 0.7347 | 0.4136 | 0.0837 | 6.8037 | 6.7441 | Sí |
| svm_c1 | 0.7740 | 0.5183 | 6.3510 | 418.6143 | 1681.6152 | No |
| svm_c10 | 0.7688 | 0.5393 | 7.6617 | 429.1537 | 1771.8809 | No |
| rf_100 | 0.7121 | 0.3377 | 0.1529 | 31.8306 | 2065.0732 | No |
| rf_300 | 0.7116 | 0.3377 | 0.3880 | 53.8300 | 6169.6045 | No |

**Resultados completos:**
`reports/green_ai_results.csv`

## Reducción dimensional y visualización

### PCA (Análisis de Componentes Principales)
PCA se aplicó únicamente al bloque de las 10 variables numéricas. Se seleccionaron 8 componentes, conservando aproximadamente el 97.84 % de la varianza acumulada.

| Configuración | F1-macro |
| :--- | :---: |
| SVM sin PCA | 0.7740 |
| SVM con PCA | 0.7734 |

La reducción dimensional produjo una diferencia absoluta de apenas 0.0006 en F1-macro, por lo que el desempeño predictivo prácticamente no se modificó.

**Figura:** `reports/pca_cumulative_variance.png`

### t-SNE (t-Distributed Stochastic Neighbor Embedding)
Se realizaron dos análisis exploratorios:

- **Estabilidad de semillas:** comparación con `perplexity=30` utilizando las semillas 42 y 7.
- **Sensibilidad a hiperparámetros:** evaluación con valores de `perplexity` en 5, 15, 30 y 50.

**Figuras:**
- `reports/tsne_two_seeds.png`
- `reports/tsne_perplexity_comparison.png`

*Las representaciones se utilizan únicamente con fines exploratorios. Las formas, distancias y agrupaciones observadas mediante t-SNE no se interpretan como validación del clasificador.*

## Green AI y frontera de Pareto

La frontera de Pareto quedó conformada por los modelos:
- **`boost`** (HistGradientBoosting)
- **`logistic`** (Logistic Regression)

### Comparación entre Logistic Regression y HistGradientBoosting

- **Ahorro en tiempo de entrenamiento:** 65.75 %
- **Reducción de tamaño en disco:** 97.98 %
- **Ahorro en tiempo de inferencia:** 49.09 %
- **Diferencia absoluta en F1-macro:** 0.0659

Dado que el F1-macro fue definido como métrica principal y `Revenue=True` como la clase prioritaria, **HistGradientBoosting** se seleccionó como la alternativa principal del experimento. **Logistic Regression** permanece como la mejor alternativa para escenarios con alta restricción de cómputo.

**Figura:** `reports/pareto.png`  
*Los tiempos obtenidos son mediciones contextuales del entorno de ejecución y no corresponden a métricas directas de consumo energético o emisiones de carbono.*

---

## Modelos serializados

Los seis modelos evaluados en el Ejercicio 02 fueron serializados mediante `joblib` y versionados en el directorio `reports/models/`:

- `boost.joblib`
- `logistic.joblib`
- `rf_100.joblib`
- `rf_300.joblib`
- `svm_c1.joblib`
- `svm_c10.joblib`

## Pruebas automatizadas

Para ejecutar la suite de pruebas desde la raíz del proyecto (PowerShell):

```powershell
$env:PYTHONPATH="src"
python -m pytest -q

### Resultado actual de las pruebas

`10 passed, 1 warning`

> **Nota sobre la advertencia:** La advertencia corresponde al uso de `SVC(probability=True)` en la versión actual de scikit-learn y no representa una falla en las pruebas.

### Cobertura de pruebas

Entre las pruebas automatizadas se incluyen:

- **Validación del entorno de trabajo:** Verificación de dependencias y versiones de Python.
- **Cumplimiento del contrato del dataset:** Validaciones de estructura, tipos de datos y ausencia de valores nulos o fuga de datos.
- **Construcción y pipeline de los modelos:** Comprobación de la correcta inicialización y transformación de datos dentro del flujo de trabajo.
- **Comportamiento y cálculo de la frontera de Pareto:** Pruebas unitarias para la función de selección de modelos óptimos bajo el enfoque Green AI.

## Artefactos principales

### Archivos CSV (Resultados y métricas)
- `reports/svm_cv_results.csv`
- `reports/lab02_model_results.csv`
- `reports/green_ai_results.csv`

### Visualizaciones y figuras
- `reports/revenue_distribution.png`
- `reports/svm_confusion_matrix.png`
- `reports/pca_cumulative_variance.png`
- `reports/tsne_two_seeds.png`
- `reports/tsne_perplexity_comparison.png`
- `reports/pareto.png`

### Modelos serializados
- `reports/models/`

## Reproducibilidad

El proyecto garantiza la reproducibilidad mediante los siguientes elementos:

- **Entorno aislado:** Uso de un entorno virtual independiente (`.venv`).
- **Gestión de dependencias:** Definición explícita de librerías y versiones en `requirements.txt`.
- **Determinismo:** Fijación de semillas aleatorias reproducibles (`random_state = 42`).
- **Estrategia de muestreo:** Partición estratificada para preservar la proporción de clases.
- **Pipelines de preprocesamiento:** Uso de `Pipeline` y `ColumnTransformer` para prevenir la fuga de información (*data leakage*).
- **Modularidad:** Código fuente reutilizable estructurado dentro de `src/`.
- **Aseguramiento de calidad:** Suite de pruebas automatizadas con `pytest`.
- **Trazabilidad de artefactos:** Almacenamiento directo de métricas, reportes y figuras dentro de `reports/`.
- **Control de versiones:** Historial gestionado con Git.

> **Tag del repositorio:** `u01-ejercicio02`


### Esta versión me parece mejor equilibrada

No eliminé nada que considero importante para los ejercicios: **instalación, ejecución, LAB01, dataset y licencia, auditoría, prevención de fuga, baseline/SVM, seis modelos, tres repeticiones, PCA, t-SNE, Green AI, Pareto, CSV, figuras, modelos serializados, pruebas y reproducibilidad**. Todos esos elementos aparecen en tu README original y están directamente relacionados con lo solicitado en las actividades. :chatgpt-content-reference{index="2"} :chatgpt-content-reference{index="3"}

Lo que eliminé principalmente fue **repetición y explicación extensa**, porque eso ya está desarrollado en los notebooks y en los dos PDFs.

Esta sería la versión que yo usaría como **README final**.