from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CARPETA_DATOS = RAIZ / "data"
CARPETA_RESULTADOS = RAIZ / "resultados"
ARCHIVO_PRECIOS = CARPETA_DATOS / "precios_semanales.csv"

INICIO = "2005-01-01"
FIN = "2025-12-31"

# 5 acciones por sector, mezclando empresas a las que les fue bien y otras que no tanto
SECTORES = {
    "Tecnología": ["AAPL", "MSFT", "INTC", "CSCO", "IBM"],
    "Salud": ["JNJ", "PFE", "MRK", "UNH", "ABT"],
    "Finanzas": ["JPM", "BAC", "WFC", "C", "GS"],
    "Energía": ["XOM", "CVX", "COP", "SLB", "OXY"],
    "Consumo básico": ["KO", "PEP", "PG", "WMT", "CL"],
    "Consumo discrecional": ["AMZN", "HD", "MCD", "NKE", "SBUX"],
    "Industria": ["CAT", "BA", "GE", "HON", "MMM"],
    "Comunicaciones": ["T", "VZ", "DIS", "CMCSA", "NFLX"],
    "Servicios públicos": ["DUK", "SO", "NEE", "D", "AEP"],
    "Materiales": ["NEM", "FCX", "SHW", "ECL", "APD"],
}

REFERENCIA = "SPY"
ACCIONES = [t for lista in SECTORES.values() for t in lista]
TICKERS = ACCIONES + [REFERENCIA]

# diseño del experimento (ver openspec/changes/diseno-del-experimento)
VENTANA = 20      # velas por imagen
HORIZONTE = 8     # semanas hacia adelante para la etiqueta
PASO = 20         # una muestra cada 20 semanas, así las imágenes no se pisan
FIN_TRAIN = "2017-06-16"
INICIO_VAL, FIN_VAL = "2018-01-01", "2020-06-12"
INICIO_TEST = "2021-01-01"
HUECO_MINIMO = 28  # semanas entre conjuntos

# extra, walk forward: 5 bloques de prueba que avanzan en el tiempo (lo sugirió un tutor en la consulta del 25/11)
WF_BLOQUES = [("2010-01-01", "2012-12-31"), ("2013-01-01", "2015-12-31"), ("2016-01-01", "2018-12-31"),
              ("2019-01-01", "2021-12-31"), ("2022-01-01", "2025-12-31")]
WF_AÑOS_ROLLING = 5        # en el rolling se entrena solo con los últimos 5 años
WF_FECHAS_VALIDACION = 3   # las últimas 3 fechas de cada entrenamiento se usan para frenar a tiempo
ARCHIVO_ETIQUETAS = CARPETA_DATOS / "etiquetas.csv"
LADO = 64          # las imágenes son de 64 x 64 píxeles
CARPETA_IMAGENES = CARPETA_DATOS / "imagenes"
