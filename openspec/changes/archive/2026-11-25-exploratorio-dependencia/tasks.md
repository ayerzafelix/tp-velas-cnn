# Tasks

## 1. Análisis exploratorio

- [x] 1.1 Escribir `src/exploratorio.py` con magnitud, dependencia por fecha y correlación por sector
- [x] 1.2 Sumar la sección al notebook
- [x] 1.3 Correr en Colab y anotar los resultados

Resultados (25/11/2026):

- Cuánto se mueve en 8 semanas. La acción sola: promedio +2,5%, mediana +2,3%, desvío 10,6%, el 10% peor −8,8% o menos y el 10% mejor +14,0% o más. Contra el SPY: promedio +0,6%, mediana +0,1%, desvío 9,4%, −9,5% y +11,2%. El 18,3% de las muestras de "sube" y el 21,0% de las de "le gana" se movieron menos de 2%: en esas la etiqueta depende de muy poco.
- ¿Se mueven juntas? En promedio sube el 60,8%. Si cada acción fuera por su lado, el % de cada fecha caería entre 47% y 75% y se saldría en alrededor del 5% de las fechas. Se sale en el 52%. La peor fecha subieron el 10% (13/08/2022) y la mejor el 98% (19/11/2011).
- Con "le gana" se sale en el 19% de las fechas (rango 37% a 65%), la peor 18% (31/12/2022) y la mejor 70% (19/01/2008). Comparar contra el SPY saca casi todo el movimiento del mercado, aunque no todo.
- Desvío del % de una fecha a otra (si fueran por su lado sería alrededor de 7): "sube" 21,5 en train, 16,8 en validación y 21,4 en test. "Le gana" 8,9, 13,5 y 14,3.
- Correlación de los rendimientos semanales: 0,54 entre dos acciones del mismo sector, 0,35 entre sectores distintos y 0,58 de cada acción con el SPY (de 0,27 en NEM a 0,79 en HON). Dentro del sector, Finanzas 0,76, Energía 0,75 y Servicios públicos 0,72 se mueven en bloque. Comunicaciones 0,36 y Materiales 0,38 son los más sueltos.
- Lectura: sin el SPY, que una acción suba depende sobre todo del mercado en esas 8 semanas, y eso no está en la foto de una sola acción. Explica por qué en la etapa 2 el año pesa más que cualquier patrón y por qué la red no pudo. Las 650 muestras de test son 13 momentos del mercado, no 650 casos independientes. Y una compra de varias acciones del mismo sector es casi una sola apuesta, como las tres petroleras de marzo de 2022 en el backtest.
