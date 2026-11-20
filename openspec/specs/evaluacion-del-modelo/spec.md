# evaluacion-del-modelo Specification

## Purpose
Define cómo separamos los datos y cómo medimos si la predicción del modelo es útil para invertir, antes de entrenar.

## Requirements

### Requirement: Split temporal con huecos
Los datos SHALL separarse por fecha en entrenamiento, validación y test, en ese orden, y MUST quedar al menos 28 semanas de hueco entre el final de un conjunto y el comienzo del siguiente. No se mezclan muestras al azar.

#### Scenario: Sin solapamiento entre conjuntos
- **WHEN** se arma el split
- **THEN** ninguna semana usada por una muestra de un conjunto, ni en su imagen ni en su etiqueta, aparece en una muestra de otro conjunto

### Requirement: Métricas del modelo
El desempeño del modelo SHALL medirse en el conjunto de test con el AUC y con la precisión en la clase "le gana".

#### Scenario: Reporte de métricas
- **WHEN** se evalúa un modelo
- **THEN** se informan su AUC y su precisión en la clase 1 sobre test

### Requirement: Baselines
Todo modelo de velas MUST compararse, con el mismo split y las mismas métricas, contra un clasificador que siempre predice la clase más frecuente y contra un modelo simple que usa solo números.

#### Scenario: La red no supera al baseline
- **WHEN** la red no supera a los baselines en test
- **THEN** se informa como resultado del trabajo

### Requirement: Backtest con costos
El proyecto SHALL simular, en el período de test, invertir en las acciones que el modelo marca como "le gana", descontando costos de transacción, y SHALL comparar el resultado con comprar SPY en el mismo período.

#### Scenario: Comparación contra SPY
- **WHEN** se corre el backtest
- **THEN** se informa el rendimiento acumulado de la estrategia y el de SPY en las mismas fechas, con los costos ya descontados
