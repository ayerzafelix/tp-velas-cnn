# Velas japonesas y redes convolucionales

Trabajo final · Ciencia de Datos (A422) · Universidad de San Andrés · 2026

## Pregunta de investigación

**¿Se puede, a partir de los patrones de velas japonesas, obtener una predicción útil para invertir con un rendimiento mayor al del S&P 500?**

Partimos de que las velas por sí solas tienen poca información sobre el futuro del precio, por eso esperamos resultados apenas por encima del azar. Aun así, creemos que algunas formas de velas pueden darle al modelo una pequeña ventaja.

## Cómo correrlo

El código vive en `src/` y se corre desde Colab, que usamos por la GPU para entrenar la red.

Abrir [`notebooks/correr_en_colab.ipynb`](https://colab.research.google.com/github/ayerzafelix/tp-velas-cnn/blob/main/notebooks/correr_en_colab.ipynb) y ejecutar todas las celdas. El notebook clona este repositorio y corre los scripts en orden.

## Documentación

Las definiciones y decisiones del trabajo están en `openspec/`, escritas con [OpenSpec](https://openspec.dev/):

| Cambio | Qué define | Estado |
|---|---|---|
| `datos-y-eda-inicial` | Descarga, calidad de los precios y estacionariedad | Terminado (archivado) |
| `diseno-del-experimento` | Target, imágenes, split, métricas, baselines y backtest | En curso: falta correr el backtest |
| `primera-red` | Primera red convolucional | Implementada, falta correr con datos reales |

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `src/` | Scripts del proyecto |
| `notebooks/` | Notebook para correr los scripts en Colab |
| `openspec/` | Especificaciones y decisiones |
| `data/` | Precios descargados (se generan con los scripts) |
| `resultados/` | Tablas y gráficos que generan los scripts |
| `docs/` | Material de apoyo |

## Uso de IA

En el desarrollo del código se utilizó Claude (Anthropic) como herramienta de apoyo, tal como lo habilitó la cátedra. La pregunta de investigación, las decisiones de diseño y el informe son de los autores.
