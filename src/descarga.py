"""Baja las velas semanales de todas las acciones y de SPY y las guarda en data/."""
import pandas as pd
import yfinance as yf

from config import ARCHIVO_PRECIOS, CARPETA_DATOS, FIN, INICIO, SECTORES, TICKERS


def descargar():
    crudo = yf.download(TICKERS, start=INICIO, end=FIN, interval="1wk",
                        auto_adjust=True, group_by="ticker", progress=False)

    # paso a formato largo: una fila por acción y semana
    filas = []
    for t in TICKERS:
        df = crudo[t][["Open", "High", "Low", "Close"]].dropna().copy()
        df["ticker"] = t
        filas.append(df)
    precios = pd.concat(filas).reset_index().rename(columns={"Date": "fecha"})
    precios.columns = [c.lower() for c in precios.columns]

    sector_de = {t: s for s, lista in SECTORES.items() for t in lista}
    precios["sector"] = precios["ticker"].map(sector_de).fillna("Índice")
    return precios


if __name__ == "__main__":
    precios = descargar()
    CARPETA_DATOS.mkdir(exist_ok=True)
    precios.to_csv(ARCHIVO_PRECIOS, index=False)

    semanas = precios.groupby("ticker")["fecha"].count()
    print("filas:", len(precios))
    print("series:", precios["ticker"].nunique(), "de", len(TICKERS))
    print("nulos:", precios.isna().sum().sum())
    print("semanas por serie: mínimo", semanas.min(), "máximo", semanas.max())
    print("desde", precios["fecha"].min(), "hasta", precios["fecha"].max())
