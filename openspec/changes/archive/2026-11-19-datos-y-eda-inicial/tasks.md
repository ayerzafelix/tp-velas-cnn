# Tasks

## 1. Estructura

- [x] 1.1 Pasar la configuración (acciones, sectores, fechas y rutas) a `src/config.py` y verificar que los demás scripts la importan
- [x] 1.2 Crear `requirements.txt` y verificar que `pip install -r requirements.txt` corre en Colab

## 2. Datos

- [x] 2.1 Escribir `src/descarga.py` y verificar que genera `data/precios_semanales.csv` con 51 series completas y sin nulos
- [x] 2.2 Escribir `src/calidad.py` y verificar que informa los tres chequeos y guarda los saltos grandes

## 3. Análisis exploratorio

- [x] 3.1 Escribir `src/estacionariedad.py` y verificar que guarda la tabla de p-valores y el gráfico de SPY

## 4. Colab

- [x] 4.1 Crear `notebooks/correr_en_colab.ipynb`, que clona el repo y corre los scripts, y sacar el notebook anterior
- [x] 4.2 Correr el notebook en Colab con los datos reales y anotar los resultados

## Resultados con datos reales (19/11)

- 51 series de 1096 semanas, sin nulos.
- Calidad: 0 velas mal armadas y 0 precios en cero o negativos.
- 22 semanas con saltos de más de 40%. Son hechos reales (16 de bancos en la crisis de 2008 y 2009, Boeing y Occidental en el COVID, Occidental en 2022 y Netflix en enero de 2013), así que se mantienen.
- Estacionariedad: el log del precio no es estacionario en ninguna de las 51 series y el log-rendimiento sí lo es en las 51.
