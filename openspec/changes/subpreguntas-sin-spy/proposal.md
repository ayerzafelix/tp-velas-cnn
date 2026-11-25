# Proposal

## Why

El 24/11 le mostramos el trabajo a Gabi. Le gustó la pregunta y lo hecho hasta ahora, y pidió que todo eso quede anotado como parte del proceso. Pero comparar solo contra el SPY le pareció poco interesante. Pidió dos cosas: probar sin el SPY, viendo si la red puede predecir si una acción sube o no, y hacer mucho análisis de datos para mostrar cómo la red entiende los patrones y que nosotros entendemos qué hace.

La pregunta principal no cambia. De ella salen subpreguntas:
1. ¿Puede la red anticipar si una acción le gana al S&P 500? (hecha, etapas anteriores)
2. ¿Funciona mejor cuando la acción viene de caer? (hecha, `iteracion-caidas`)
3. ¿Puede anticipar algo más básico, si la acción sube o no, sin compararla con nada? (este cambio)
4. ¿Qué patrones usa la red para decidir? (este cambio)

## What Changes

- Etiqueta nueva "sube": log-rendimiento de la acción del cierre de t al cierre de t+8 mayor a 0. Es el único cambio. Imágenes, split, red y 10 corridas quedan iguales.
- Análisis de la etiqueta nueva por conjunto, sector y año.
- Baselines con la etiqueta nueva y la red en 10 corridas.
- Análisis de patrones: para cada imagen de test se describe hacia dónde venía la acción, el color de la última vela, si la última vela forma un patrón con nombre del material de velas (doji, martillo, envolvente) y la volatilidad, y se compara lo que dice la red con lo que pasó, también por sector y por año.
- Mapa de calor sobre la red nueva.

## Capabilities

### New Capabilities
- `prediccion-sube`: la subpregunta de si la acción sube.
- `patrones-de-la-red`: qué patrones usa la red y si acierta con ellos.

### Modified Capabilities

## Impact

- `src/etiquetas.py` agrega las columnas `rend_absoluto` y `sube`, sin cambiar lo anterior.
- `src/red.py`: `cargar` acepta qué columna usar como etiqueta.
- `src/baselines.py`: la función de variables agrega el rendimiento de las 20 semanas sin restar SPY.
- `src/mapa_calor.py` acepta el argumento `sube` para usar la red nueva.
- Scripts nuevos `src/sube.py` y `src/patrones.py`.
