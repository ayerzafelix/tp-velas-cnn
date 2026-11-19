# Tasks

## 1. Etiquetas

- [x] 1.1 Calcular el rendimiento relativo a SPY de t a t+8 y la etiqueta, y verificar el caso de ejemplo de la spec
- [x] 1.2 Asignar cada muestra a entrenamiento, validación o test con los huecos de 28 semanas y verificar que no se comparte ninguna semana
- [x] 1.3 Informar el balance de clases total, por sector y por conjunto

Resultados con datos reales (19/11): 2.600 muestras (1.600 train, 350 validación, 650 test), huecos de 40 semanas entre conjuntos. Le ganan al SPY el 50,7% en total, 51,1% en train, 46,3% en validación y 52,0% en test, así que las clases quedan balanceadas. Por sector va de 40,0% en Energía a 57,3% en Finanzas.

## 2. Imágenes

- [ ] 2.1 Dibujar las imágenes de 20 velas con la escala normalizada y sin elementos extra, y revisar a ojo una muestra
- [ ] 2.2 Verificar que la última vela de cada imagen es la de la semana t

## 3. Baselines

- [ ] 3.1 Entrenar los dos baselines y reportar AUC y precisión en la clase 1 sobre test

## 4. Backtest

- [ ] 4.1 Implementar el backtest con costos y verificarlo con un caso chico calculado a mano
