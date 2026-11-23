# Tasks

## 1. Mapa de calor

- [x] 1.1 Guardar la red en `src/red.py`
- [x] 1.2 Escribir `src/mapa_calor.py` con Grad-CAM, los ejemplos y la atención por vela
- [x] 1.3 Correr en Colab, revisar los gráficos y anotar los resultados

## Resultados con datos reales (23/11)

- La atención promedio por vela va de 4,6% a 5,3%, casi pareja en las 20 velas. Las últimas 5 se llevan el 24,8%, igual que si mirara todo parejo. La red no se concentra en las últimas semanas ni en ninguna zona en particular.
- Las predicciones más seguras de la red son 0,54 para "le gana" y 0,42 para "no le gana". La red casi nunca se aleja de 0,5, o sea que no está segura de nada.
- En los ejemplos de "le gana" el mapa queda casi vacío. En los de "no le gana" la atención sigue las velas más largas, que son las semanas de más movimiento.
- Como la red no tiene una ventaja real, el mapa muestra en qué se fija pero no un patrón que sirva para invertir.
