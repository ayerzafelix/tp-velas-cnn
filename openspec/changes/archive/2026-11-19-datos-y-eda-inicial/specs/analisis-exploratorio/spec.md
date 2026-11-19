# Spec Delta

## Purpose

Reúne los análisis que hacemos sobre las series de precios antes de modelar, para justificar con datos las decisiones de diseño.

## ADDED Requirements

### Requirement: Estacionariedad de las series
El proyecto SHALL evaluar con el test ADF, para cada serie, si el logaritmo del precio y el log-rendimiento semanal son estacionarios, tomando como estacionaria una serie con p-valor menor a 0,05.

#### Scenario: Resultado por serie
- **WHEN** se corre el análisis de estacionariedad
- **THEN** se guarda en `resultados/estacionariedad.csv` el p-valor de las dos versiones de cada serie y se informa cuántas series son estacionarias en cada caso

#### Scenario: Gráfico de referencia
- **WHEN** se corre el análisis de estacionariedad
- **THEN** se guarda un gráfico de SPY con el logaritmo del precio y el log-rendimiento semanal en `resultados/estacionariedad_spy.png`
