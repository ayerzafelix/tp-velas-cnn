# Spec Delta

## Purpose

Muestra qué parte de las imágenes usa la red para decidir.

## ADDED Requirements

### Requirement: Mapa de calor por imagen
El proyecto SHALL calcular con Grad-CAM, para cada imagen de test, un mapa de qué zonas empujan a la red hacia la clase que eligió, y SHALL mostrar las tres imágenes en las que la red está más segura de cada clase.

#### Scenario: Ejemplos
- **WHEN** se corre el mapa de calor
- **THEN** se guarda `resultados/mapa_calor_ejemplos.png` con cada imagen y su mapa encima

### Requirement: Atención por vela
El proyecto SHALL informar qué porcentaje de la atención promedio cae en cada una de las 20 velas, de la más vieja a la de la semana t.

#### Scenario: Velas más miradas
- **WHEN** se corre el mapa de calor
- **THEN** se informa el porcentaje de cada vela, cuánto se llevan las últimas 5 y se guarda `resultados/mapa_calor_por_vela.png`
