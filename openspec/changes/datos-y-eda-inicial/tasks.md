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
- [ ] 4.2 Correr el notebook en Colab con los datos reales y anotar los resultados en el informe
