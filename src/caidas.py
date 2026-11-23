"""Iteración: ¿la red sirve en una situación puntual, cuando la acción viene de caer entre 5% y 10%?
Usamos la misma red de las 10 corridas y solo miramos los casos de test que vienen de esa caída."""
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, roc_auc_score

from config import ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_RESULTADOS

SEMANAS_CAIDA = 4
CAIDA_MIN, CAIDA_MAX = -0.10, -0.05

if __name__ == "__main__":
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    precios = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])
    cierres = precios.pivot(index="fecha", columns="ticker", values="close").sort_index()
    posicion = {f: i for i, f in enumerate(cierres.index)}

    # cuánto cayó cada acción en las 4 semanas anteriores a la foto
    m["caida_4s"] = [cierres[t].iloc[posicion[f]] / cierres[t].iloc[posicion[f] - SEMANAS_CAIDA] - 1
                     for t, f in zip(m["ticker"], m["fecha"])]
    m["en_caida"] = m["caida_4s"].between(CAIDA_MIN, CAIDA_MAX)

    print(f"muestras que vienen de caer entre {-CAIDA_MAX:.0%} y {-CAIDA_MIN:.0%} en {SEMANAS_CAIDA} semanas")
    print(m.groupby("conjunto")["en_caida"].agg(muestras="sum", de_cada_100=lambda x: round(x.mean() * 100, 1))
          .reindex(["train", "validacion", "test"]).to_string())

    test = m[m["conjunto"] == "test"]
    sub = test[test["en_caida"]]
    vs_spy = lambda x: (np.exp(x) - 1).mean() * 100
    print(f"\nen test, le ganan al SPY: {sub['etiqueta'].mean():.1%} de las que vienen de caer "
          f"contra {test['etiqueta'].mean():.1%} de todas")
    print(f"rinden en promedio {vs_spy(sub['rend_relativo']):+.2f}% contra SPY las que vienen de caer "
          f"y {vs_spy(test['rend_relativo']):+.2f}% todas")

    # la red de las 10 corridas, mirando solo esos casos
    p = pd.read_csv(CARPETA_RESULTADOS / "predicciones_red_10.csv", parse_dates=["fecha"])
    p = p.merge(test[["ticker", "fecha", "en_caida"]], on=["ticker", "fecha"])
    p = p[p["en_caida"]]
    filas = []
    for semilla, g in p.groupby("semilla"):
        dice = g["prob"] > 0.5
        filas.append({"semilla": semilla,
                      "auc": roc_auc_score(g["etiqueta"], g["prob"]),
                      "precision_le_gana": precision_score(g["etiqueta"], dice, zero_division=0),
                      "elige": int(dice.sum()),
                      "elegidas_vs_spy_%": vs_spy(g.loc[dice, "rend_relativo"]) if dice.any() else np.nan,
                      "descartadas_vs_spy_%": vs_spy(g.loc[~dice, "rend_relativo"]) if (~dice).any() else np.nan})
    res = pd.DataFrame(filas)
    resumen = res.drop(columns="semilla").agg(["mean", "min", "max"]).T
    resumen.columns = ["promedio", "mínimo", "máximo"]
    print(f"\nla red en los {len(sub)} casos de test que vienen de caer (10 corridas)")
    print(resumen.round(3).to_string())
    print(f"\npara comparar: decir siempre le gana en estos casos da precisión {sub['etiqueta'].mean():.3f} y AUC 0,5")
    print("corridas con AUC mayor a 0,5:", int((res["auc"] > 0.5).sum()), "de", len(res))
    print("corridas con precisión mayor a decir siempre le gana:", int((res["precision_le_gana"] > sub["etiqueta"].mean()).sum()), "de", len(res))

    res.to_csv(CARPETA_RESULTADOS / "caidas_10_corridas.csv", index=False)
