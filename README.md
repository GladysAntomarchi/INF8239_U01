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
