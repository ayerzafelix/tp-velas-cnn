"""Mira de cerca lo que hace la red en las 10 corridas: cuánto se equivoca, qué acciones elige
y si nuestras 50 acciones ya le ganan al SPY por sí solas."""
import numpy as np
import pandas as pd

from backtest import simular
from baselines import variables
from config import ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_RESULTADOS, REFERENCIA

CASOS = {
    (1, 1): "dijo le gana y le ganó",
    (1, 0): "dijo le gana y no le ganó",
    (0, 0): "dijo no y no le ganó",
    (0, 1): "dijo no y le ganó",
}


def pct(x):
    # el rendimiento relativo está en logaritmo, lo paso a % contra SPY
    return (np.exp(x) - 1) * 100


if __name__ == "__main__":
    p = pd.read_csv(CARPETA_RESULTADOS / "predicciones_red_10.csv", parse_dates=["fecha"])
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    precios = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])
    cierres = precios.pivot(index="fecha", columns="ticker", values="close").sort_index()

    p["dice"] = (p["prob"] > 0.5).astype(int)
    p["caso"] = [CASOS[(d, e)] for d, e in zip(p["dice"], p["etiqueta"])]
    p["vs_spy_%"] = pct(p["rend_relativo"])

    # 1. cuánto se equivoca: promedio de las 10 corridas para cada tipo de acierto y error
    por_caso = p.groupby(["semilla", "caso"]).agg(muestras=("vs_spy_%", "size"), vs_spy_prom=("vs_spy_%", "mean"))
    por_caso = por_caso.groupby("caso").mean().reindex(list(CASOS.values()))
    print("1. TAMAÑO DEL ERROR (promedio de las 10 corridas)")
    print("vs_spy_prom: cuánto rindió en promedio la acción contra SPY en esas 8 semanas, en %")
    print(por_caso.round(1).to_string())

    elegidas = p.groupby(["semilla", "dice"])["vs_spy_%"].mean().unstack().mean()
    print(f"\nlas que la red elige rinden en promedio {elegidas[1]:+.2f}% contra SPY")
    print(f"las que la red descarta rinden en promedio {elegidas[0]:+.2f}% contra SPY")
    print(f"todas las de test rinden en promedio {p[p['semilla'] == 0]['vs_spy_%'].mean():+.2f}% contra SPY")

    # 2. qué elige: volatilidad y sector de las elegidas contra las descartadas
    test = m[m["conjunto"] == "test"].copy()
    test["volatilidad_%"] = variables(test, precios)["volatilidad"] * 100
    p = p.merge(test[["ticker", "fecha", "volatilidad_%"]], on=["ticker", "fecha"])
    vol = p.groupby(["semilla", "dice"])["volatilidad_%"].mean().unstack().mean()
    print("\n2. QUÉ ACCIONES ELIGE")
    print(f"volatilidad semanal promedio de las elegidas: {vol[1]:.2f}%")
    print(f"volatilidad semanal promedio de las descartadas: {vol[0]:.2f}%")

    compras = p[p["dice"] == 1].groupby(["semilla", "sector"]).size()
    sectores = (compras / compras.groupby("semilla").transform("sum") * 100).groupby("sector").mean()
    sectores = sectores.sort_values(ascending=False).round(1).rename("% de las compras")
    print("\nde qué sector son las compras (si eligiera al azar, cada sector sería 10%)")
    print(sectores.to_string())

    # 3. sesgo de selección: ¿las 50 acciones juntas ya le ganan al SPY, sin ninguna red?
    filas = []
    for conjunto in ["train", "validacion", "test"]:
        c = m[m["conjunto"] == conjunto]
        fechas = sorted(c["fecha"].unique())
        las_50, _ = simular(c[["ticker", "fecha"]].assign(prob=1.0), cierres)
        spy, _ = simular(pd.DataFrame({"ticker": REFERENCIA, "fecha": fechas, "prob": 1.0}), cierres)
        gana_por_fecha = c.groupby("fecha")["rend_relativo"].apply(lambda x: (np.exp(x) - 1).mean() > 0)
        filas.append({"conjunto": conjunto, "períodos": len(fechas),
                      "las_50_%": round(las_50 * 100, 1), "spy_%": round(spy * 100, 1),
                      "% períodos que las 50 le ganan": round(gana_por_fecha.mean() * 100, 1),
                      "% muestras que le ganan": round(c["etiqueta"].mean() * 100, 1)})
    sesgo = pd.DataFrame(filas)
    print("\n3. SESGO DE SELECCIÓN: comprar las 50 por igual contra SPY, sin red")
    print(sesgo.to_string(index=False))

    por_caso.round(2).to_csv(CARPETA_RESULTADOS / "analisis_tamano_error.csv")
    sectores.to_csv(CARPETA_RESULTADOS / "analisis_sectores.csv")
    sesgo.to_csv(CARPETA_RESULTADOS / "analisis_sesgo_seleccion.csv", index=False)
