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
- `notebooks/`: notebooks de Jupyter.
- `reports/`: reportes y resultados.
- `src/`: código fuente.
- `tests/`: pruebas unitarias.

## Creación y activación del entorno virtual

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.venv\Scripts\Activate.ps1

## Instalación de dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Ejecución de pruebas
$env:PYTHONPATH="src"
python -m pytest -q

## Resultado obtenido
1 passed

## LAB01 · SVM con pipeline y validación cruzada

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