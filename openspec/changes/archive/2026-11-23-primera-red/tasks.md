# Tasks

## 1. Red

- [x] 1.1 Escribir `src/red.py` con la arquitectura de la spec y verificar que entrena y guarda las predicciones de test
- [x] 1.2 Correr en Colab y anotar las métricas de test y las curvas de entrenamiento
- [x] 1.3 Comparar contra los baselines y en el backtest
- [x] 1.4 Desarmar el backtest de la red por período y por acción para ver de dónde sale el 54,7%
- [x] 1.5 Escribir `src/varias_corridas.py`, que entrena la red 10 veces con semillas distintas
- [x] 1.6 Correr las 10 corridas en Colab y anotar promedio, mínimo y máximo
- [x] 1.7 Revisar qué acciones elige la red: volatilidad, sector y rendimiento de las elegidas contra las descartadas (pasa al cambio `analisis-de-la-red`, junto con lo que pidió el tutor)

## Resultados con datos reales (20/11)

- Entrenó 7 épocas y se quedó con la segunda. Desde ahí la pérdida de entrenamiento baja y la de validación sube, o sea que la red empieza a memorizar el entrenamiento.
- Test: AUC 0,451 y precisión en "le gana" 0,457, diciendo "le gana" 105 veces de 650. No supera a los baselines (precisión 0,520 diciendo siempre "le gana").
- Backtest en test (13 períodos de 8 semanas desde el 30/01/2021): red 54,7%, siempre "le gana" 20,5%, regresión logística 16,2% y SPY 9,8%. El resultado de la red no cuadra con sus métricas, así que hay que ver de qué períodos y acciones sale antes de sacar conclusiones.

## Segunda corrida y detalle del backtest (20/11)

- Al volver a entrenar la red, el backtest pasó de 54,7% a 5,6%, con 137 compras en vez de 105. SPY 9,8%, regresión logística 16,2% y comprar siempre las 50 acciones 20,5% no cambian porque no dependen del entrenamiento.
- El resultado de la red no es estable entre corridas. El entrenamiento en GPU no da exactamente igual cada vez y con 13 períodos cualquier diferencia pesa mucho.
- Hay períodos con 1 a 3 compras que mueven todo el resultado, por ejemplo -20,9% con una sola acción en noviembre de 2021 y +16,1% con tres petroleras en marzo de 2022.
- Las compras que más aportaron fueron XOM, SLB y COP en marzo de 2022, la suba del petróleo por la guerra en Ucrania, y PFE en junio de 2021.
- Conclusión: el 54,7% de la primera corrida fue suerte. La red no tiene una ventaja estable sobre los baselines ni sobre SPY.

## Diez corridas (20/11)

Tercera corrida suelta de `red.py`: AUC 0,445 y precisión 0,459, diciendo "le gana" 181 veces de 650.

Resumen de las 10 corridas en test:

| Métrica | Promedio | Mínimo | Máximo |
|---|---|---|---|
| AUC | 0,486 | 0,457 | 0,513 |
| Precisión en "le gana" | 0,515 | 0,473 | 0,621 |
| Compras | 314 | 29 | 644 |
| Backtest | 41,6% | 22,8% | 59,0% |

- AUC mayor a 0,5 en 1 de 10 corridas. Precisión mayor a 0,520 en 4 de 10. Para clasificar, la red queda en el nivel del azar.
- Backtest mayor al de SPY (9,8%) en 10 de 10 corridas y mayor al de comprar siempre las 50 acciones (20,5%) también en 10 de 10.
- Las dos cosas no cuadran. Si la red no separa bien las que le ganan al SPY, la ventaja en plata tiene que venir de otro lado, por ejemplo de que elige acciones que se mueven más y en este período eso pagó. Las 10 corridas comparten los mismos 13 períodos, así que miden el azar del entrenamiento y no el del mercado. Hay que revisar qué acciones elige antes de sacar conclusiones.
