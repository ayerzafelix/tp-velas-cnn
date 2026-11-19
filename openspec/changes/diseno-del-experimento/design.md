# Design

## Context

Los precios ya están descargados y revisados (ver el cambio `datos-y-eda-inicial`). Este diseño fija los números concretos que piden las specs, para que queden decididos antes de entrenar.

## Goals / Non-Goals

**Goals:**
- Tener todas las definiciones del experimento escritas antes de entrenar.

**Non-Goals:**
- Elegir la arquitectura de la red. Se decide en un cambio aparte.

## Decisions

**Fechas del split.** Tomamos como fecha de cada muestra la semana t.
- Entrenamiento: t hasta el 16/06/2017.
- Validación: t del 01/01/2018 al 12/06/2020.
- Test: t desde el 01/01/2021.

Entrenamos con los años más viejos y probamos con los más nuevos, así el test simula usar el modelo en el futuro.

**Huecos de 28 semanas.** Cada muestra usa 20 semanas para la imagen y 8 para la etiqueta. Con 28 semanas de hueco ninguna semana queda compartida entre dos conjuntos. Un hueco de solo 8 semanas cubría la etiqueta pero no la imagen.

**Costos del backtest.** Suponemos un costo de 0,1% por cada compra y por cada venta. Es un supuesto nuestro y se puede revisar.

**Mecánica del backtest.** Cada 8 semanas, dentro del período de test, compramos en partes iguales todas las acciones que el modelo marca como "le gana", las mantenemos 8 semanas y las vendemos. Comparamos contra comprar SPY y mantenerlo durante el mismo período.

**Una muestra cada 20 semanas.** Gabi pidió que las fotos no se solapen demasiado. Con un paso igual al largo de la imagen, dos fotos seguidas de la misma acción no comparten ninguna vela, y como el horizonte es de 8 semanas tampoco comparten etiqueta. Quedan unas 2.600 muestras en total, dentro de lo que pidieron los tutores (1.500 a 2.000 o más).

**Precios en logaritmo en las imágenes.** El análisis de estacionariedad mostró que el log-rendimiento es estacionario en las 51 series y el log del precio en ninguna. Dibujamos las velas con el logaritmo de los precios para que una suba de 10% se vea igual en cualquier acción y en cualquier momento.

**Formato de la imagen.** 64 x 64 píxeles a color, con fondo negro, velas alcistas en verde y bajistas en rojo. Cada vela ocupa 3 píxeles de ancho, así entran las 20. Guardamos cada imagen como PNG en una carpeta por conjunto y por clase.

**Umbral.** El modelo marca "le gana" cuando la probabilidad es mayor a 0,5.

**Baseline numérico.** Una regresión logística con dos variables calculadas sobre las mismas 20 semanas de la imagen: el log-rendimiento de la acción menos el de SPY, y la volatilidad de la acción.

## Risks / Trade-offs

- [Sesgo de supervivencia] Elegimos acciones que existen hoy y que cotizan desde 2005, así que quedan afuera las que quebraron o salieron del índice. Con los datos que usamos no lo podemos corregir → lo informamos como limitación.
- [Datos menos independientes] Las 50 acciones se mueven juntas con el mercado, así que la información real es menor que la cantidad de muestras → lo informamos como limitación y miramos los resultados por período.
- [La volatilidad cambia en el tiempo] Aunque los log-rendimientos sean estacionarios, en las crisis se mueven mucho más → lo tenemos en cuenta al leer los resultados por período.

