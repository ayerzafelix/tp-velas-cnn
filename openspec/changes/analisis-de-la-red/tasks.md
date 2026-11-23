# Tasks

## 1. Análisis

- [x] 1.1 Guardar las predicciones de test de cada una de las 10 corridas
- [x] 1.2 Escribir `src/analisis_red.py` con el tamaño del error, la volatilidad y los sectores de lo que elige la red, y el sesgo de selección
- [x] 1.3 Correr en Colab y anotar los resultados

## Resultados con datos reales (23/11)

Tamaño del error, promedio de las 10 corridas:

| Caso | Muestras | Contra SPY |
|---|---|---|
| Dijo le gana y le ganó | 140,4 | +8,7% |
| Dijo le gana y no le ganó | 136,4 | -7,4% |
| Dijo no y no le ganó | 175,6 | -7,6% |
| Dijo no y le ganó | 197,6 | +8,1% |

- Los errores son del mismo tamaño que los aciertos, unos 8 puntos para cada lado.
- Las que la red elige rinden +0,84% contra SPY, las que descarta +0,80% y todas las de test +0,76%. En promedio, la red no elige acciones mejores que las que descarta.

Qué elige:
- Volatilidad semanal de las elegidas 3,89% contra 3,57% de las descartadas. Elige acciones algo más riesgosas.
- Por sector, sus compras van de 8,6% a 11,0%, cerca del 10% que daría elegir al azar. No se concentra en ningún sector.

Sesgo de selección, comprar las 50 por igual contra SPY:

| Conjunto | Períodos | Las 50 | SPY | Períodos que las 50 le ganan |
|---|---|---|---|---|
| Train | 32 | 135,5% | 86,5% | 68,8% |
| Validación | 7 | 10,2% | 14,9% | 42,9% |
| Test | 13 | 20,5% | 9,8% | 61,5% |

- Las 50 le ganan al SPY en entrenamiento y en test sin ninguna red. El sesgo que marcó el tutor existe y va como limitación. La comparación justa para la red es contra comprar las 50.
- Como la red no elige acciones mejores que las que descarta, su ventaja en el backtest frente a comprar las 50 no viene de elegir acciones. Tiene que venir de cuántas compra en cada uno de los 13 períodos, y con tan pocos períodos eso no es confiable.
