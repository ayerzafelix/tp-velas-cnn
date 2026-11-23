# Proposal

## Why

Con las imágenes, las etiquetas y los baselines listos, falta la primera red convolucional que mire las velas y diga si la acción le gana al S&P 500. El profesor dejó libre la arquitectura. Arrancamos con una red chica, parecida a las que armamos en clase, para tener un primer resultado contra los baselines.

## What Changes

- Una red convolucional en Keras que recibe la imagen de 64 x 64 y devuelve la probabilidad de que la acción le gane al SPY.
- Entrenamiento con el conjunto de entrenamiento, frenando con el de validación, y evaluación en test con las métricas definidas.
- Las predicciones de test pasan al backtest junto con las de los baselines.

## Capabilities

### New Capabilities
- `modelo-de-velas`: la red que clasifica las imágenes de velas.

### Modified Capabilities

## Impact

- Script nuevo `src/red.py`. Usa TensorFlow, que ya viene instalado en Colab.
