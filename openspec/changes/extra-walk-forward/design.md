# Design

## Bloques

Cinco bloques de prueba de 3 años (el último de 4, hasta 2025). Con bloques de un año quedarían unas 130 imágenes por prueba, muy pocas. Con estos quedan entre 350 y 500. El primer bloque empieza en 2010 para que haya al menos 5 años para entrenar.

## Sin data leakage

Igual que en el corte único: entre la última fecha de entrenamiento y la primera de prueba hay al menos 28 semanas (20 de la imagen más 8 del horizonte), así ninguna semana se comparte.

## Validación

La red sigue frenando con EarlyStopping, así que cada entrenamiento necesita su validación. Usamos las últimas 3 fechas del período de entrenamiento (150 imágenes) y dejamos el mismo hueco de 28 semanas entre lo que entrena y lo que valida.

## Números que elegimos nosotros

Nadie fijó estos números y se pueden cambiar en `src/config.py`: los años de cada bloque, 5 años para el rolling y 3 fechas de validación.

## Lo que hay que tener en cuenta

- En el primer bloque el rolling y el extendido son iguales, porque los datos arrancan en 2005.
- Los primeros bloques entrenan con pocas imágenes (unas 350) y el rolling siempre entrena con pocas (entre 350 y 450). Es parte de lo que se compara: más pasado contra pasado más reciente.
- Si en un bloque la red nunca dice que sí, su precisión queda vacía en vez de 0.
- Son 200 entrenamientos (5 bloques, 2 esquemas, 2 etiquetas, 10 corridas). En Colab con GPU tarda bastante más que lo anterior.
