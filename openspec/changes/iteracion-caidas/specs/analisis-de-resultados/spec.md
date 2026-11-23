# Spec Delta

## ADDED Requirements

### Requirement: Evaluación en acciones que vienen de caer
El proyecto SHALL evaluar la red de las 10 corridas solo en los casos de test en los que la acción cayó entre 5% y 10% en las 4 semanas anteriores a la semana t, con AUC, precisión en "le gana" y rendimiento contra SPY de las elegidas y las descartadas, y SHALL informar cuántas muestras de ese tipo hay en cada conjunto.

#### Scenario: Comparación en la situación puntual
- **WHEN** se evalúa la red en los casos que vienen de caer
- **THEN** se compara contra decir siempre "le gana" en esos mismos casos y se informa en cuántas de las 10 corridas la red lo supera
