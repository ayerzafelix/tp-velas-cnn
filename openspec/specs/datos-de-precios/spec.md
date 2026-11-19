# datos-de-precios Specification

## Purpose
Define qué precios usa el proyecto, de dónde salen y qué controles tienen que pasar antes de usarse para armar imágenes y etiquetas.

## Requirements

### Requirement: Universo de acciones
El proyecto SHALL usar 50 acciones del S&P 500, 5 por cada uno de 10 sectores, mezclando en cada sector empresas a las que les fue bien y otras a las que les fue peor, más SPY como referencia del índice.

#### Scenario: Series descargadas
- **WHEN** se corre la descarga
- **THEN** quedan 51 series, una por cada acción y una para SPY, cada una con su sector

### Requirement: Velas semanales ajustadas
Cada serie SHALL tener velas semanales (apertura, máximo, mínimo y cierre) desde enero de 2005 hasta diciembre de 2025, con precios ajustados por dividendos. No se usa volumen.

#### Scenario: Serie completa
- **WHEN** se revisa una serie descargada
- **THEN** tiene la misma cantidad de semanas que las demás y ningún valor faltante

### Requirement: Control de calidad
Antes de usar los precios el proyecto MUST verificar que el máximo de cada vela no quede por debajo de la apertura o el cierre, que el mínimo no quede por encima, que no haya precios en cero o negativos, y MUST listar las semanas con saltos de más de 40% para revisarlas.

#### Scenario: Precios válidos
- **WHEN** se corre el control de calidad
- **THEN** informa cuántas velas fallan cada chequeo y guarda la lista de saltos grandes en `resultados/saltos_semanales.csv`
