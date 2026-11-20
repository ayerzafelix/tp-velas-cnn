# Tasks

## 1. Etiquetas

- [x] 1.1 Calcular el rendimiento relativo a SPY de t a t+8 y la etiqueta, y verificar el caso de ejemplo de la spec
- [x] 1.2 Asignar cada muestra a entrenamiento, validación o test con los huecos de 28 semanas y verificar que no se comparte ninguna semana
- [x] 1.3 Informar el balance de clases total, por sector y por conjunto

Resultados con datos reales (19/11): 2.600 muestras (1.600 train, 350 validación, 650 test), huecos de 40 semanas entre conjuntos. Le ganan al SPY el 50,7% en total, 51,1% en train, 46,3% en validación y 52,0% en test, así que las clases quedan balanceadas. Por sector va de 40,0% en Energía a 57,3% en Finanzas.

## 2. Imágenes

- [x] 2.1 Dibujar las imágenes de 20 velas con la escala normalizada y sin elementos extra, y revisar a ojo una muestra
- [x] 2.2 Verificar que la última vela de cada imagen es la de la semana t

Resultados con datos reales (20/11): 2.600 imágenes de 64 x 64. Train 818 de clase 1 y 782 de clase 0, validación 162 y 188, test 338 y 312. Revisamos a ojo 12 ejemplos y se ven las 20 velas sin ejes ni etiquetas. El script verifica en cada imagen que la última vela sea la de la semana t.

## 3. Baselines

- [x] 3.1 Entrenar los dos baselines y reportar AUC y precisión en la clase 1 sobre test

Resultados en test (20/11), 650 muestras, 338 le ganan al SPY:
- Siempre la clase más frecuente (dice siempre "le gana"): AUC 0,500 y precisión 0,520.
- Regresión logística con rendimiento contra SPY y volatilidad de las 20 semanas: AUC 0,507 y precisión 0,513, diciendo "le gana" 476 veces.

La regresión logística queda en el nivel del azar y no supera a decir siempre "le gana". La vara para la red es una precisión mayor a 0,520 y un AUC mayor a 0,5.

## 4. Backtest

- [ ] 4.1 Implementar el backtest con costos y verificarlo con un caso chico calculado a mano
