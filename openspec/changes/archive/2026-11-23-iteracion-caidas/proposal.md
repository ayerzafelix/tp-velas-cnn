# Proposal

## Why

La red no sirve para elegir acciones en general. Puede que sí sirva en una situación puntual. Los tutores marcaron que las preguntas acotadas suelen funcionar mejor, y al principio del trabajo nos preguntamos si una caída de 5% a 10% es una corrección después de la cual la acción rebota. Probamos si la red acierta más en esos casos.

## What Changes

- Marcar las muestras en las que la acción cayó entre 5% y 10% en las 4 semanas anteriores a la foto.
- Medir la red de las 10 corridas solo en los casos de test que cumplen eso, con las mismas métricas y comparada contra decir siempre "le gana" en esos mismos casos.
- Es un solo cambio: la red, el entrenamiento y las imágenes son los mismos. No entrenamos una red solo con caídas porque en entrenamiento hay pocas muestras de ese tipo.

## Capabilities

### New Capabilities

### Modified Capabilities
- `analisis-de-resultados`: suma la evaluación en una situación puntual.

## Impact

- Script nuevo `src/caidas.py`.
