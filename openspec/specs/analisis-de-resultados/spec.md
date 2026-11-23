# analisis-de-resultados Specification

## Purpose
Explica qué hace la red más allá de sus métricas y qué sesgos tiene el dataset, para leer bien los resultados.

## Requirements

### Requirement: Tamaño del error
Para las 10 corridas, el proyecto SHALL informar cuántas muestras caen en cada tipo de acierto y de error y cuánto rindieron en promedio contra SPY, en porcentaje, además del rendimiento promedio contra SPY de las acciones que la red elige y de las que descarta.

#### Scenario: Error que cuesta plata
- **WHEN** la red dice que una acción le gana al SPY y no le gana
- **THEN** se informa cuánto quedó abajo del SPY en promedio esa clase de error

### Requirement: Qué acciones elige la red
El proyecto SHALL comparar la volatilidad semanal promedio de las acciones que la red elige con la de las que descarta, y SHALL informar de qué sectores son sus compras.

#### Scenario: Red que elige acciones más riesgosas
- **WHEN** la volatilidad de las elegidas es mayor que la de las descartadas
- **THEN** queda a la vista que la red toma más riesgo que elegir al azar

### Requirement: Sesgo de selección
El proyecto SHALL medir, en entrenamiento, validación y test, el rendimiento de comprar las 50 acciones por igual contra el de SPY con la misma mecánica del backtest, y el porcentaje de períodos en que las 50 le ganan al SPY.

#### Scenario: Acciones que ya le ganan al índice
- **WHEN** las 50 acciones juntas le ganan al SPY sin usar ninguna red
- **THEN** el resultado de la red se compara contra comprar las 50 y no solo contra SPY, y el sesgo se informa como limitación

### Requirement: Evaluación en acciones que vienen de caer
El proyecto SHALL evaluar la red de las 10 corridas solo en los casos de test en los que la acción cayó entre 5% y 10% en las 4 semanas anteriores a la semana t, con AUC, precisión en "le gana" y rendimiento contra SPY de las elegidas y las descartadas, y SHALL informar cuántas muestras de ese tipo hay en cada conjunto.

#### Scenario: Comparación en la situación puntual
- **WHEN** se evalúa la red en los casos que vienen de caer
- **THEN** se compara contra decir siempre "le gana" en esos mismos casos y se informa en cuántas de las 10 corridas la red lo supera
