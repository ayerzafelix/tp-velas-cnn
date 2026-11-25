# Tasks

## 1. Subpregunta 3: ¿sube?

- [x] 1.1 Agregar la etiqueta "sube" en `src/etiquetas.py` sin cambiar lo anterior
- [x] 1.2 Escribir `src/sube.py`: balance por conjunto, sector y año, baselines y red en 10 corridas
- [x] 1.3 Correr en Colab y anotar los resultados

Resultados (25/11/2026):

- Una acción sube en 8 semanas el 60,8% de las veces (train 63,4%, validación 56,0%, test 57,1%). Por sector va de 51,2% (Energía) a 67,3% (Consumo básico).
- Por año cambia mucho más que por cualquier otra cosa: en test va de 29,3% (2022) a 82,0% (2023).
- Baselines en test (650 muestras, 371 suben): decir siempre "sube" da AUC 0,5 y precisión 0,571. La regresión logística da AUC 0,5 y precisión 0,567, y dice "sube" en 645 de 650.
- Red en 10 corridas: dice "sube" en las 650 imágenes en las 10 corridas, así que su precisión es 0,571, igual a decir siempre "sube". AUC 0,444 (0,416 a 0,467), menor a 0,5 en las 10. La mejor época es la 1 en 7 de las 10 corridas (promedio 1,6).
- Lectura: la red aprendió que las acciones suben más de lo que bajan y nada más. El AUC por debajo de 0,5 en las 10 corridas dice que, cuando le da más probabilidad a una imagen que a otra, en test pasa al revés.

## 2. Subpregunta 4: ¿qué patrones usa?

- [x] 2.1 Escribir `src/patrones.py` con tendencia, color y patrón de la última vela, volatilidad, sector y año
- [x] 2.2 Permitir el mapa de calor sobre la red nueva
- [x] 2.3 Correr en Colab y anotar los resultados
- [x] 2.4 Cambiar la tabla para mostrar la probabilidad que le da la red en vez de cuántas veces dice "sube"
- [x] 2.5 Volver a correr en Colab y anotar los resultados

Resultados de la primera corrida (25/11/2026):

- Como la red dice "sube" en todas, la columna "cuántas veces dice sube" quedó en 100% en todos los grupos y "acierta" quedó igual a "sube de verdad". Con eso no se ve qué aprendió. Por eso en 2.4 cambiamos a la probabilidad promedio que le da la red (va de 0,54 a 0,67), que sí varía entre imágenes.
- Lo que sí se ve es que varios patrones se dan vuelta entre train y test:
  - Tendencia: en train subían menos las que venían de subir más de 10% (56,0% contra 65,7% a 69,4% del resto). En test esas son las que más suben (61,1%) y las que menos suben son las que subieron hasta 10% (48,4%).
  - Color de la última vela: en train subían más después de una vela roja (66,4% contra 60,9%). En test pasa al revés (53,3% roja contra 59,8% verde).
  - Envolvente bajista: en train subía el 61,5%, en test el 42,9% (35 muestras). En test se comporta como dice el material de velas, en train no.
  - Martillos: 7 y 7 muestras en test, muy pocas para sacar algo.
- La volatilidad es lo único que se mantiene: las de volatilidad baja suben más en train (67,0%) y en test (65,9%) que las de media y alta (alrededor de 55% en test).
- Mapa de calor de la red nueva: las últimas 5 velas se llevan el 24,3% de la atención (25% si mirara parejo). Las probabilidades de la red de la semilla 0 van de 0,53 a 0,84, nunca baja de 0,5. De las 3 imágenes con probabilidad más alta, 2 no subieron.

Resultados con la probabilidad de la red (25/11/2026):

- La probabilidad promedio va de 0,54 a 0,67. Entre grupos se mueve muy poco, como mucho 4 puntos.
- Tendencia: es lo que más la mueve. La red le da más probabilidad a las que bajaron hasta 10% (61,9%) y menos a las que subieron más de 10% (57,9%), el mismo orden que en train (69,4% y 56,0%). En test las que subieron más de 10% son las que más suben (61,1%). La red aprendió "si ya subió mucho, sube menos" y entre 2021 y 2025 pasó lo contrario. Eso explica el AUC menor a 0,5.
- Color: la red le da un poco más a la vela roja (60,5% contra 59,7%), como en train. En test pasa al revés.
- Patrones del material (doji, martillo, envolvente): la probabilidad va de 58,6% a 60,6%, casi igual que "ninguno" (60,0%). La red no los usa.
- Volatilidad: es lo único que se mantiene de train a test (las de volatilidad baja suben más), pero la red no lo toma: le da menos probabilidad a las de volatilidad baja (59,3%). Cada imagen está escalada para ocupar todo el alto, así que una acción que se movió poco y una que se movió mucho se ven parecidas.
- Sector y año: la red casi no cambia (59,5% a 60,5% por sector, 59,4% a 61,4% por año). En 2022 subió el 29,3% de las acciones y la red siguió diciendo "sube" con 60,4%.
