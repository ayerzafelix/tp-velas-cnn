# Spec Delta

## ADDED Requirements

### Requirement: Bloques de prueba que avanzan en el tiempo
El proyecto SHALL evaluar la red en 5 bloques de prueba consecutivos (2010 a 2012, 2013 a 2015, 2016 a 2018, 2019 a 2021 y 2022 a 2025), definidos en `src/config.py`, usando las mismas imágenes y la misma red que el corte único.

#### Scenario: Cada bloque se prueba por separado
- **WHEN** se evalúa un bloque
- **THEN** la red se entrena solo con fechas anteriores a ese bloque y se prueba solo con las fechas del bloque

### Requirement: Extendido y rolling
El proyecto SHALL entrenar cada bloque de dos formas: extendido, con todas las fechas anteriores, y rolling, con las fechas de los últimos 5 años.

#### Scenario: Primer bloque
- **WHEN** el bloque es 2010 a 2012
- **THEN** extendido y rolling usan las mismas fechas, porque los datos empiezan en 2005

### Requirement: Sin data leakage
El proyecto MUST dejar al menos 28 semanas entre la última fecha de entrenamiento y la primera de prueba, y entre la última fecha de entrenamiento y la primera de validación.

#### Scenario: Hueco antes de la prueba
- **WHEN** el bloque de prueba empieza en la fecha t
- **THEN** ninguna muestra de entrenamiento tiene fecha posterior a t menos 28 semanas

### Requirement: Evaluación y promedio
El proyecto SHALL entrenar la red 10 veces por bloque, esquema y etiqueta (le gana y sube), informar AUC y precisión de cada bloque junto con la regresión logística de antes entrenada con las mismas fechas, y SHALL informar el promedio de los 5 bloques. Los resultados se guardan en `resultados/walk_forward.csv`, `resultados/walk_forward_corridas.csv` y `resultados/walk_forward.png`.

#### Scenario: Comparación con el azar y el baseline
- **WHEN** se resume cada esquema
- **THEN** se informa en cuántos bloques la red supera AUC 0,5 y en cuántos supera a la regresión logística
