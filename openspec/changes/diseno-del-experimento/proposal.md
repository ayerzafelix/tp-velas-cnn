# Proposal

## Why

La pregunta del trabajo es si se puede, a partir de los patrones de velas japonesas, obtener una predicción útil para invertir con un rendimiento mayor al del S&P 500. El profesor nos pidió definir antes de entrenar qué significa "útil", contra qué comparamos, en qué ventana y cómo lo calculamos, y cuidar el split temporal, los baselines y el formato de las imágenes.

## What Changes

- Definición del target: rendimiento de la acción contra el de SPY del cierre de la semana t al cierre de la semana t+8.
- Definición de las imágenes: 20 velas semanales, escala normalizada en cada imagen, sin ejes ni etiquetas y sin volumen.
- Definición de la evaluación: split temporal con huecos, métricas del modelo, baselines simples y un backtest con costos en un período que el modelo no vio.

## Capabilities

### New Capabilities
- `definicion-del-target`: cómo se calcula la etiqueta "le gana al S&P 500".
- `imagenes-de-velas`: cómo se dibuja cada imagen que ve la red.
- `evaluacion-del-modelo`: cómo se separan los datos y cómo se mide si la predicción es útil.

### Modified Capabilities

## Impact

- Scripts futuros en `src/` para armar etiquetas, imágenes, baselines, entrenamiento y backtest.
- Las definiciones quedan fijas antes de entrenar. Si alguna cambia, se registra como un cambio nuevo.
