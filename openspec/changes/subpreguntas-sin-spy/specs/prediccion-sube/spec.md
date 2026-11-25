# Spec Delta

## Purpose

Evalúa si la red puede anticipar si una acción sube en las 8 semanas siguientes, sin compararla con el SPY.

## ADDED Requirements

### Requirement: Etiqueta "sube"
Para cada muestra el proyecto SHALL calcular el log-rendimiento de la acción del cierre de la semana t al cierre de la semana t+8, y la etiqueta "sube" SHALL valer 1 si es mayor a 0 y 0 en otro caso. Las imágenes, el split y la red MUST ser los mismos que en las etapas anteriores.

#### Scenario: Acción que sube
- **WHEN** una acción pasa de 100 a 103 entre t y t+8
- **THEN** su etiqueta "sube" es 1, sin importar lo que hizo el SPY

### Requirement: Balance y comparación
El proyecto SHALL informar el porcentaje de muestras que suben en total, por conjunto, por sector y por año, y SHALL comparar la red en 10 corridas contra decir siempre la clase más frecuente y contra una regresión logística con el rendimiento y la volatilidad de las 20 semanas, con AUC y precisión en "sube".

#### Scenario: Muchas más subas que bajas
- **WHEN** las acciones suben más seguido de lo que bajan
- **THEN** la red solo aporta si supera la precisión de decir siempre "sube"
