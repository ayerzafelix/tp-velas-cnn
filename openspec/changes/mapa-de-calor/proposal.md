# Proposal

## Why

Gabi pidió como bonus mostrar qué miró la red para decidir. Con Grad-CAM vemos qué parte de cada imagen empuja a la red hacia "le gana" o hacia "no le gana", y qué velas mira más en promedio.

## What Changes

- Guardar la red que entrena `src/red.py`.
- Calcular el mapa de Grad-CAM de cada imagen de test, mostrar ejemplos y la atención promedio por vela.

## Capabilities

### New Capabilities
- `interpretacion-de-la-red`: qué mira la red en las imágenes.

### Modified Capabilities

## Impact

- `src/red.py` guarda la red en `resultados/red.keras`.
- Script nuevo `src/mapa_calor.py`.
