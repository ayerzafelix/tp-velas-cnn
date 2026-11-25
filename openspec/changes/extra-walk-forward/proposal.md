# Proposal

## Why

Esto es un extra, no algo que pidió Gabi. En la consulta del 25/11 un tutor nos marcó que train (2005 a 2017), validación (2018 a 2020) y test (2021 a 2025) caen en contextos económicos distintos. Ya lo habíamos visto en los datos: lo que la red aprende en un período se da vuelta en el siguiente, y el año pesa más que cualquier patrón. Con un solo corte, el resultado depende de qué años nos tocaron para probar. El tutor nos sugirió averiguar walk forward, en sus dos versiones (extendido y rolling), y promediar los resultados.

## What Changes

- En vez de un solo corte, 5 bloques de prueba que avanzan en el tiempo: 2010 a 2012, 2013 a 2015, 2016 a 2018, 2019 a 2021 y 2022 a 2025.
- Extendido: para cada bloque se entrena con todo lo anterior. Rolling: solo con los últimos 5 años.
- Se hace con las dos etiquetas, le gana y sube.
- Misma red, mismas imágenes, 10 corridas por bloque, la misma regresión logística como baseline, y al final el promedio de los 5 bloques.
- No cambia nada de lo anterior. El corte único sigue siendo el resultado principal.

## Capabilities

### New Capabilities
- `walk-forward`: evaluación en 5 bloques que avanzan en el tiempo, extendido y rolling.

### Modified Capabilities

## Impact

- Script nuevo `src/walk_forward.py` y parámetros nuevos en `src/config.py`.
- Sección nueva "Extra: walk forward" al final del notebook.
