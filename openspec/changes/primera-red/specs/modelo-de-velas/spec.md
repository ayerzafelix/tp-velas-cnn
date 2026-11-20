# Spec Delta

## Purpose

Define la red convolucional que mira las imágenes de velas y cómo se entrena y evalúa.

## ADDED Requirements

### Requirement: Arquitectura inicial
La red SHALL recibir imágenes de 64 x 64 a color y tener tres capas convolucionales con max pooling (16, 32 y 64 filtros de 3 x 3), una capa densa de 64 neuronas con dropout de 0,5 y una salida sigmoide.

#### Scenario: Salida de la red
- **WHEN** la red recibe una imagen
- **THEN** devuelve un número entre 0 y 1, la probabilidad de que la acción le gane al SPY

### Requirement: Entrenamiento sin mirar el test
La red SHALL entrenarse solo con el conjunto de entrenamiento y MUST usar el de validación para frenar el entrenamiento cuando la pérdida de validación deja de mejorar durante 5 épocas, quedándose con la mejor época. El conjunto de test MUST NOT usarse hasta la evaluación final.

#### Scenario: Frenado temprano
- **WHEN** la pérdida de validación no mejora en 5 épocas seguidas
- **THEN** el entrenamiento se corta y se recuperan los pesos de la mejor época

### Requirement: Evaluación comparable
La red SHALL evaluarse en test con las mismas métricas que los baselines y sus predicciones SHALL pasar al backtest.

#### Scenario: Reporte de la red
- **WHEN** termina el entrenamiento
- **THEN** se informan el AUC y la precisión en la clase "le gana" sobre test y se guardan las predicciones en `resultados/predicciones_red.csv`

### Requirement: Resultados sobre varias corridas
Como el resultado de la red cambia entre entrenamientos, la red SHALL entrenarse 10 veces con semillas distintas y sus métricas y su backtest SHALL informarse con el promedio, el mínimo y el máximo de esas corridas. Cualquier mejora futura MUST compararse de la misma forma.

#### Scenario: Comparación contra la vara
- **WHEN** terminan las 10 corridas
- **THEN** se informa en cuántas la precisión supera a decir siempre "le gana", en cuántas el AUC supera 0,5 y en cuántas el backtest supera a SPY
