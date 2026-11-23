# Tasks

## 1. Iteración

- [x] 1.1 Escribir `src/caidas.py` que marca las caídas de 5% a 10% en 4 semanas y evalúa la red en esos casos
- [x] 1.2 Correr en Colab y anotar los resultados

## Resultados con datos reales (23/11)

- Muestras que vienen de caer entre 5% y 10% en 4 semanas: 178 en train (11,1%), 21 en validación (6,0%) y 80 en test (12,3%).
- En test le ganan al SPY el 52,5% de las que vienen de caer contra 52,0% de todas, y rinden +1,78% contra SPY contra +0,76% de todas.
- La red en esos 80 casos, 10 corridas: AUC promedio 0,542 (0,436 a 0,624), mayor a 0,5 en 8 de 10. Precisión promedio 0,520 contra 0,525 de decir siempre "le gana", la supera en 5 de 10. Las elegidas rinden +1,47% contra SPY y las descartadas +1,26%.
- En esta situación la red ordena un poco mejor que el azar, pero con 80 casos esa diferencia está dentro de lo que puede dar la suerte, y no elige acciones que rindan más. No alcanza para decir que sea útil.
