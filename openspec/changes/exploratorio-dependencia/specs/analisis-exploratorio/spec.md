# Spec Delta

## ADDED Requirements

### Requirement: Magnitud de los movimientos
El proyecto SHALL informar cuánto se mueve una acción en las 8 semanas siguientes, sola y contra el SPY, con promedio, mediana, desvío, el 10% peor, el 10% mejor y el porcentaje de muestras que se movió menos de 2%.

#### Scenario: Muestras que casi no se movieron
- **WHEN** una muestra se movió menos de 2% en las 8 semanas
- **THEN** se cuenta aparte, porque su etiqueta depende de muy poco

### Requirement: Dependencia entre acciones
El proyecto SHALL informar, para cada fecha de muestra, el porcentaje de las 50 acciones que sube y el que le gana al SPY, y SHALL compararlo con el rango que tendría si cada acción se moviera por su lado (la proporción promedio más y menos dos desvíos de una binomial con 50 casos).

#### Scenario: Fechas en que se mueven juntas
- **WHEN** el porcentaje de una fecha cae fuera de ese rango
- **THEN** se cuenta como fecha en que las acciones se movieron juntas

### Requirement: Correlación entre sectores
El proyecto SHALL calcular la correlación de los log-rendimientos semanales entre acciones del mismo sector, de sectores distintos y de cada acción con el SPY, y SHALL guardar la correlación promedio por par de sectores en `resultados/exploratorio_correlacion.csv` con su gráfico.

#### Scenario: Matriz por sector
- **WHEN** se corre el análisis
- **THEN** se guarda `resultados/exploratorio_correlacion.png` con la correlación promedio entre cada par de sectores
