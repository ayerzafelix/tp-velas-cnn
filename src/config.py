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
