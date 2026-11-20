# imagenes-de-velas Specification

## Purpose
Define cómo se dibuja cada imagen de velas que recibe la red, para que todas sean comparables y no tengan información extra.

## Requirements

### Requirement: Ventana de la imagen
Cada imagen SHALL mostrar las 20 velas semanales que terminan en la semana t, y MUST NOT incluir ninguna vela posterior a t.

#### Scenario: Imagen sin futuro
- **WHEN** se arma la imagen de la semana t
- **THEN** la última vela dibujada es la de la semana t

### Requirement: Imágenes que no se pisan
Dentro de una misma acción, las imágenes MUST NOT compartir velas. Se toma una muestra cada 20 semanas, en las mismas fechas para todas las acciones.

#### Scenario: Dos muestras seguidas de una acción
- **WHEN** se toman dos muestras consecutivas de la misma acción
- **THEN** sus semanas t están separadas por 20 semanas y sus imágenes no tienen ninguna vela en común

### Requirement: Escala normalizada
La escala de precio de cada imagen SHALL ir del mínimo al máximo de las 20 velas que muestra, con los precios en logaritmo, para que el nivel de precio de la acción no influya y las subas y bajas se vean en proporción.

#### Scenario: Acciones de distinto precio
- **WHEN** dos acciones tienen la misma forma de velas pero una cotiza a 10 y otra a 500
- **THEN** sus imágenes son iguales

### Requirement: Imagen sin elementos extra
Las imágenes MUST NOT tener ejes, etiquetas, títulos, grilla ni volumen, y SHALL tener todas el mismo tamaño en píxeles.

#### Scenario: Formato de la imagen
- **WHEN** se revisa cualquier imagen generada
- **THEN** solo se ven las velas, sobre un fondo uniforme y con el mismo tamaño que las demás
