# Proposal

## Why

Para responder si los patrones de velas japonesas sirven para invertir con un rendimiento mayor al del S&P 500 primero necesitamos precios confiables de muchas acciones y entender cómo se comportan esas series. El profesor nos pidió además revisar si las series son estacionarias y si conviene usar una transformación logarítmica.

## What Changes

- Descarga de velas semanales de 2005 a 2025 de 50 acciones del S&P 500 (5 por sector en 10 sectores) y de SPY como referencia, con precios ajustados por dividendos.
- Chequeo de calidad de los precios descargados.
- Análisis de estacionariedad con el test ADF sobre el logaritmo del precio y sobre el log-rendimiento semanal.
- El código pasa de un notebook a scripts en `src/`. Colab queda solo para correrlos.

## Capabilities

### New Capabilities
- `datos-de-precios`: obtención y validación de las velas semanales que usa todo el proyecto.
- `analisis-exploratorio`: análisis de las series de precios antes de modelar.

### Modified Capabilities

## Impact

- Scripts nuevos: `src/config.py`, `src/descarga.py`, `src/calidad.py`, `src/estacionariedad.py`.
- Notebook nuevo `notebooks/correr_en_colab.ipynb`, que reemplaza a `notebooks/01_descarga_y_eda.ipynb`.
- Dependencias en `requirements.txt`: yfinance, pandas, numpy, statsmodels y matplotlib.
