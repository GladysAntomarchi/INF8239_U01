# Ficha del dataset

## Dataset seleccionado

**Online Shoppers Purchasing Intention**

## Formulación del problema

- **Dominio:** Comercio electrónico / comportamiento de clientes.
- **Unidad de análisis:** Una sesión de navegación de un visitante en un sitio de comercio electrónico.
- **Decisión que se desea apoyar:** Identificar sesiones con probabilidad de finalizar en una compra.
- **Target:** `Revenue`.
- **Tipo de tarea:** Clasificación binaria.
- **Clases:** `False` = no finaliza en compra; `True` = finaliza en compra.
- **Error más costoso:** No identificar una sesión que finalmente termina en compra (`Revenue=True`), debido a la pérdida de oportunidad de reconocer oportunamente una intención de compra.
- **Usuario de la solución:** Analista de comercio electrónico, marketing digital o gestión comercial.

## Pregunta de análisis

¿En qué medida las características de navegación de una sesión permiten predecir si esta finalizará en una compra?

## Candidatos aprobados

| Criterio | Online Shoppers Purchasing Intention | Dry Bean |
|---|---|---|
| Procedencia | UCI Machine Learning Repository | UCI Machine Learning Repository |
| Licencia | CC BY 4.0 | CC BY 4.0 |
| Filas | 12,330 | 13,611 |
| Predictores | 17 | 16 |
| Target | `Revenue` | `Class` |
| Clases | 2 | 7 |
| Valores ausentes reportados | No | No |
| Tipo de clasificación | Binaria | Multiclase |
| Tamaño compatible con CPU/Colab | Sí | Sí |

## Selección

Se seleccionó **Online Shoppers Purchasing Intention** como dataset principal por presentar un problema de clasificación natural, un tamaño adecuado para los experimentos posteriores y una combinación de variables numéricas y categóricas.

- Ficha oficial:
  https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset

- Segunda alternativa:
  https://archive.ics.uci.edu/dataset/602/dry+bean

## Tamizaje inicial

El dataset original contiene 12,330 registros. Se identificaron 125 registros duplicados exactos, que fueron eliminados mediante código antes de realizar la partición de entrenamiento y prueba.

Después de la limpieza quedaron 12,205 observaciones y no se identificaron valores ausentes.

La variable `Revenue` presenta desbalance de clases:

- `False`: 84.37 %
- `True`: 15.63 %

Por este motivo se utilizará **F1-macro** como métrica principal y una partición 80/20 estratificada.

## Antecedente de selección

Inicialmente se había considerado el dataset Disease Prediction Using Machine Learning. Durante su auditoría se identificaron 4,616 registros duplicados de 4,920, quedando solamente 304 observaciones únicas. Debido al elevado riesgo de contaminación entre entrenamiento y prueba, se solicitó al docente la sustitución del dataset, la cual fue aprobada.