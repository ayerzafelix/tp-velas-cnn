"""Chequea si las series son estacionarias, en precio y en log-rendimiento."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from statsmodels.tsa.stattools import adfuller

from config import ARCHIVO_PRECIOS, CARPETA_RESULTADOS, REFERENCIA

warnings.filterwarnings("ignore", category=FutureWarning)

if __name__ == "__main__":
    p = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"]).sort_values(["ticker", "fecha"])
    p["log_precio"] = np.log(p["close"])
    p["log_rend"] = p.groupby("ticker")["log_precio"].diff()

    # test ADF: si el p-valor es menor a 0,05 tomamos la serie como estacionaria
    filas = []
    for t, g in p.groupby("ticker"):
        filas.append({
            "ticker": t,
            "sector": g["sector"].iloc[0],
            "p_valor_log_precio": adfuller(g["log_precio"])[1],
            "p_valor_log_rend": adfuller(g["log_rend"].dropna())[1],
        })
    res = pd.DataFrame(filas)
    res["estacionaria_log_precio"] = res["p_valor_log_precio"] < 0.05
    res["estacionaria_log_rend"] = res["p_valor_log_rend"] < 0.05

    n = len(res)
    print(f"log del precio estacionario en {res['estacionaria_log_precio'].sum()} de {n} series")
    print(f"log-rendimiento estacionario en {res['estacionaria_log_rend'].sum()} de {n} series")

    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    res.round(4).to_csv(CARPETA_RESULTADOS / "estacionariedad.csv", index=False)

    # gráfico de SPY: precio en log vs log-rendimiento semanal
    spy = p[p["ticker"] == REFERENCIA]
    fig, ax = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
    ax[0].plot(spy["fecha"], spy["log_precio"], color="tab:blue")
    ax[0].set_title("SPY: log del precio (tiene tendencia, no es estacionaria)")
    ax[1].plot(spy["fecha"], spy["log_rend"], color="tab:gray", linewidth=0.7)
    ax[1].axhline(0, color="black", linewidth=0.5)
    ax[1].set_title("SPY: log-rendimiento semanal (gira alrededor de 0)")
    fig.tight_layout()
    fig.savefig(CARPETA_RESULTADOS / "estacionariedad_spy.png", dpi=120)
    print("gráfico guardado en resultados/estacionariedad_spy.png")
