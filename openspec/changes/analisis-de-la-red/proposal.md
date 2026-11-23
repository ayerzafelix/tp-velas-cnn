# Proposal

## Why

En las 10 corridas la red no clasifica mejor que el azar pero gana plata en el backtest, y no sabemos por qué. Además un tutor nos marcó dos cosas. Primero, que al predecir solo "le gana o no" escondemos cuánto se equivoca la red: no es lo mismo elegir una acción que quedó 1% abajo del SPY que una que quedó 10% abajo. Segundo, que las empresas que elegimos pueden estar sesgadas, porque si son empresas que ya le ganan al S&P 500 por sí solas la red no aporta nada.

## What Changes

- Medir el tamaño del error: cuánto rindieron contra SPY, en promedio, las acciones de cada tipo de acierto y de error.
- Ver qué acciones elige la red: su volatilidad y su sector, contra las que descarta.
- Medir el sesgo de selección: si comprar las 50 acciones por igual, sin red, ya le gana al SPY en entrenamiento, validación y test.
- Todo sobre las 10 corridas de la red, sin modelos nuevos.

## Capabilities

### New Capabilities
- `analisis-de-resultados`: análisis de lo que hace la red y de los sesgos del dataset.

### Modified Capabilities

## Impact

- `src/varias_corridas.py` guarda además las predicciones de test de cada corrida.
- Script nuevo `src/analisis_red.py`.
