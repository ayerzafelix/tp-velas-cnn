# Spec Delta

## Purpose

Fija de forma concreta qué significa que una acción le gane al S&P 500, para que la etiqueta sea la misma en todo el proyecto.

## ADDED Requirements

### Requirement: Rendimiento relativo a SPY
Para cada acción y semana t, el proyecto SHALL calcular el log-rendimiento de la acción del cierre de la semana t al cierre de la semana t+8 y restarle el log-rendimiento de SPY en la misma ventana.

#### Scenario: Cálculo del rendimiento relativo
- **WHEN** una acción pasa de 100 a 110 entre t y t+8 y SPY pasa de 400 a 420
- **THEN** el rendimiento relativo es log(110/100) menos log(420/400), aproximadamente 0,046

### Requirement: Etiqueta binaria
La etiqueta SHALL valer 1 ("le gana") si el rendimiento relativo es mayor a 0 y 0 en cualquier otro caso. Las semanas sin 8 semanas posteriores disponibles MUST quedar sin etiqueta.

#### Scenario: Acción que le gana al índice
- **WHEN** el rendimiento relativo da mayor a 0
- **THEN** la etiqueta es 1

#### Scenario: Final de la serie
- **WHEN** la semana t está entre las últimas 8 semanas de datos
- **THEN** esa semana no se usa como muestra

### Requirement: Balance de clases
El proyecto MUST informar la proporción de cada clase en total, por sector y por conjunto (entrenamiento, validación y test).

#### Scenario: Reporte de balance
- **WHEN** se arman las etiquetas
- **THEN** se informa el porcentaje de etiquetas 1 y 0 en cada caso
