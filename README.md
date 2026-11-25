# Velas japonesas y redes convolucionales

Trabajo final · Ciencia de Datos (A422) · Universidad de San Andrés · 2026

## Pregunta de investigación

**¿Se puede, a partir de los patrones de velas japonesas, obtener una predicción útil para invertir con un rendimiento mayor al del S&P 500?**

Partimos de que las velas por sí solas tienen poca información sobre el futuro del precio, por eso esperamos resultados apenas por encima del azar. Aun así, creemos que algunas formas de velas pueden darle al modelo una pequeña ventaja.

## Subpreguntas

De la pregunta principal salen subpreguntas que fuimos respondiendo en orden:

1. ¿Puede la red anticipar si una acción le gana al S&P 500?
2. ¿Funciona mejor cuando la acción viene de caer entre 5% y 10%?
3. ¿Puede anticipar algo más básico, si la acción sube o no, sin compararla con nada?
4. ¿Qué patrones usa la red para decidir?

## Cómo correrlo

El código vive en `src/` y se corre desde Colab, que usamos por la GPU para entrenar la red.

Abrir [`notebooks/correr_en_colab.ipynb`](https://colab.research.google.com/github/ayerzafelix/tp-velas-cnn/blob/main/notebooks/correr_en_colab.ipynb) y ejecutar todas las celdas. El notebook clona este repositorio y corre los scripts en orden.

## Documentación

Las definiciones y decisiones del trabajo están en `openspec/`, escritas con [OpenSpec](https://openspec.dev/):

| Cambio | Qué define | Estado |
|---|---|---|
| `datos-y-eda-inicial` | Descarga, calidad de los precios y estacionariedad | Terminado |
| `diseno-del-experimento` | Target, imágenes, split, métricas, baselines y backtest | Terminado |
| `primera-red` | Primera red convolucional y evaluación en 10 corridas | Terminado |
| `analisis-de-la-red` | Tamaño del error, qué elige la red y sesgo de selección | Terminado |
| `iteracion-caidas` | La red en acciones que vienen de caer 5% a 10% | Terminado |
| `mapa-de-calor` | Qué mira la red (Grad-CAM) | Terminado |
| `subpreguntas-sin-spy` | Subpreguntas 3 y 4: si la acción sube y qué patrones usa la red | Terminado |
| `exploratorio-dependencia` | Cuánto se mueven las acciones y cuánto se mueven juntas | Implementado, falta correr |

Los cambios terminados están en `openspec/changes/archive/` y las especificaciones vigentes en `openspec/specs/`.

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
