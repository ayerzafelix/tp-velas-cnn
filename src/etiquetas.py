"""Arma una muestra por acción cada 20 semanas, con su etiqueta y su conjunto."""
import numpy as np
import pandas as pd

from config import (ACCIONES, ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_RESULTADOS,
                    FIN_TRAIN, FIN_VAL, HORIZONTE, HUECO_MINIMO, INICIO_TEST, INICIO_VAL,
                    PASO, REFERENCIA, VENTANA)


def rendimiento_relativo(accion_t, accion_th, spy_t, spy_th):
    # log-rendimiento de la acción menos el de SPY, de t a t+8
    return np.log(accion_th / accion_t) - np.log(spy_th / spy_t)


def conjunto_de(fecha):
    if fecha <= pd.Timestamp(FIN_TRAIN):
        return "train"
    if pd.Timestamp(INICIO_VAL) <= fecha <= pd.Timestamp(FIN_VAL):
        return "validacion"
    if fecha >= pd.Timestamp(INICIO_TEST):
        return "test"
    return "hueco"


if __name__ == "__main__":
    # chequeo con el ejemplo de la spec
    assert abs(rendimiento_relativo(100, 110, 400, 420) - 0.0465) < 0.001

    p = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])
    cierres = p.pivot(index="fecha", columns="ticker", values="close").sort_index()
    sector_de = p.drop_duplicates("ticker").set_index("ticker")["sector"]
    fechas = cierres.index

    # la primera muestra necesita 20 velas para atrás y la última 8 semanas para adelante
    posiciones = range(VENTANA - 1, len(fechas) - HORIZONTE, PASO)
    filas = []
    for i in posiciones:
        for t in ACCIONES:
            rel = rendimiento_relativo(cierres[t].iloc[i], cierres[t].iloc[i + HORIZONTE],
                                       cierres[REFERENCIA].iloc[i], cierres[REFERENCIA].iloc[i + HORIZONTE])
            filas.append({"ticker": t, "sector": sector_de[t], "fecha": fechas[i],
                          "posicion": i, "rend_relativo": rel, "etiqueta": int(rel > 0)})
    m = pd.DataFrame(filas)
    m["conjunto"] = m["fecha"].apply(conjunto_de)
    print("muestras armadas:", len(m), "| quedan en el hueco:", (m["conjunto"] == "hueco").sum())
    m = m[m["conjunto"] != "hueco"]

    # chequeo de huecos: semanas entre la última muestra de un conjunto y la primera del siguiente
    orden = ["train", "validacion", "test"]
    for a, b in zip(orden, orden[1:]):
        hueco = m.loc[m["conjunto"] == b, "posicion"].min() - m.loc[m["conjunto"] == a, "posicion"].max()
        print(f"hueco entre {a} y {b}: {hueco} semanas (mínimo {HUECO_MINIMO})")
        assert hueco >= HUECO_MINIMO

    m.drop(columns="posicion").to_csv(ARCHIVO_ETIQUETAS, index=False)

    # balance de clases
    print("\n% que le gana al SPY")
    print("total:", round(m["etiqueta"].mean() * 100, 1), "% de", len(m), "muestras")
    por_conjunto = m.groupby("conjunto")["etiqueta"].agg(muestras="count", pct_le_gana="mean").reindex(orden)
    por_sector = m.groupby("sector")["etiqueta"].agg(muestras="count", pct_le_gana="mean")
    for tabla in (por_conjunto, por_sector):
        tabla["pct_le_gana"] = (tabla["pct_le_gana"] * 100).round(1)
        print("\n" + tabla.to_string())

    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    pd.concat([por_conjunto.assign(grupo="conjunto"), por_sector.assign(grupo="sector")]).to_csv(
        CARPETA_RESULTADOS / "balance_clases.csv")
