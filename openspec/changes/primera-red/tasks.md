# Tasks

## 1. Red

- [x] 1.1 Escribir `src/red.py` con la arquitectura de la spec y verificar que entrena y guarda las predicciones de test
- [x] 1.2 Correr en Colab y anotar las métricas de test y las curvas de entrenamiento
- [x] 1.3 Comparar contra los baselines y en el backtest
- [ ] 1.4 Desarmar el backtest de la red por período y por acción para ver de dónde sale el 54,7%

## Resultados con datos reales (20/11)

- Entrenó 7 épocas y se quedó con la segunda. Desde ahí la pérdida de entrenamiento baja y la de validación sube, o sea que la red empieza a memorizar el entrenamiento.
- Test: AUC 0,451 y precisión en "le gana" 0,457, diciendo "le gana" 105 veces de 650. No supera a los baselines (precisión 0,520 diciendo siempre "le gana").
- Backtest en test (13 períodos de 8 semanas desde el 30/01/2021): red 54,7%, siempre "le gana" 20,5%, regresión logística 16,2% y SPY 9,8%. El resultado de la red no cuadra con sus métricas, así que hay que ver de qué períodos y acciones sale antes de sacar conclusiones.
