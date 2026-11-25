# Spec Delta

## Purpose

Muestra qué características de las velas asocia la red con "sube" y si esa asociación se cumple.

## ADDED Requirements

### Requirement: Patrones contra predicciones
Para cada imagen de test el proyecto SHALL describir hacia dónde venía la acción en las 20 semanas, el color de la última vela, si la última vela es un doji, un martillo (separando si venía de bajar), una envolvente alcista o una envolvente bajista, y la volatilidad, y SHALL informar para cada grupo cuántas subían en entrenamiento, la probabilidad promedio que le dan las 10 redes de que suba y cuántas suben de verdad en test.

#### Scenario: Patrón que la red usa
- **WHEN** la red le da más probabilidad de subir a un grupo que a otro
- **THEN** se ve si ese grupo subía más en entrenamiento y si sube más de verdad en test

### Requirement: Dónde acierta y dónde no
El proyecto SHALL informar los mismos números por sector y por año de test.

#### Scenario: Años de crisis
- **WHEN** en un año la mayoría de las acciones baja
- **THEN** se ve si la red lo detecta o sigue diciendo "sube"

### Requirement: Mapa de calor de la red nueva
El proyecto SHALL correr el mapa de calor sobre una de las redes que predicen "sube".

#### Scenario: Atención por vela
- **WHEN** se corre el mapa de calor con el argumento `sube`
- **THEN** se guardan los ejemplos y la atención por vela con el sufijo `_sube`
