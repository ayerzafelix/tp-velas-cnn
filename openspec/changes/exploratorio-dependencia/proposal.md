# Proposal

## Why

Gabi pidió mucho análisis de datos y en su devolución sobre la pregunta marcó que los datos son menos independientes de lo que parecen, porque las 50 acciones se mueven juntas con el mercado. Hasta ahora lo teníamos solo como limitación, sin medirlo. Pedro marcó que lo binario esconde cuánto se movió la acción. La etapa sin el SPY mostró que el año pesa más que cualquier patrón (en 2022 subió el 29% de las acciones y en 2023 el 82%). Este cambio mide las dos cosas con los datos.

## What Changes

- Cuánto se mueve una acción en las 8 semanas siguientes, sola y contra el SPY: promedio, mediana, desvío, extremos y cuántas casi no se movieron.
- En cada fecha de muestra, qué porcentaje de las 50 sube y qué porcentaje le gana al SPY, comparado con el rango que tendría si cada acción se moviera por su lado.
- Correlación de los rendimientos semanales entre acciones del mismo sector, de sectores distintos y con el SPY.
- No cambia nada del modelo. Es solo análisis exploratorio.

## Capabilities

### New Capabilities

### Modified Capabilities
- `analisis-exploratorio`: suma la magnitud de los movimientos y la dependencia entre acciones.

## Impact

- Script nuevo `src/exploratorio.py`.
- Sección nueva al final del notebook.
