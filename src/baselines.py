"""Baselines: modelos simples contra los que después comparamos la red."""
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from config import ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_RESULTADOS, REFERENCIA, VENTANA


def variables(m, precios):
    """Para cada muestra, dos números de las mismas 20 semanas que ve la imagen."""
    cierres = precios.pivot(index="fecha", columns="ticker", values="close").sort_index()
    log_rend = np.log(cierres).diff()
    filas = []
    for _, r in m.iterrows():
        ventana = log_rend.loc[:r["fecha"]].tail(VENTANA - 1)   # 19 cambios entre las 20 velas
        filas.append({
            "rend_vs_spy": ventana[r["ticker"]].sum() - ventana[REFERENCIA].sum(),
            "rend_20s": ventana[r["ticker"]].sum(),
            "volatilidad": ventana[r["ticker"]].std(),
        })
    return pd.DataFrame(filas, index=m.index)


if __name__ == "__main__":
    precios = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    X = variables(m, precios)[["rend_vs_spy", "volatilidad"]]
    y = m["etiqueta"]
    train, test = m["conjunto"] == "train", m["conjunto"] == "test"

    modelos = {
        "siempre la clase más frecuente": DummyClassifier(strategy="most_frequent"),
        "regresión logística (rendimiento vs SPY y volatilidad)": make_pipeline(StandardScaler(), LogisticRegression()),
    }
    filas, predicciones = [], []
    for nombre, modelo in modelos.items():
        modelo.fit(X[train], y[train])
        prob = modelo.predict_proba(X[test])[:, 1]
        pred = (prob > 0.5).astype(int)
        predicciones.append(m.loc[test, ["ticker", "fecha"]].assign(modelo=nombre, prob=prob))
        filas.append({
            "modelo": nombre,
            "auc_test": round(roc_auc_score(y[test], prob), 3),
            "precision_le_gana_test": round(precision_score(y[test], pred, zero_division=0), 3),
            "veces_que_dice_le_gana": int(pred.sum()),
        })
    res = pd.DataFrame(filas)
    print("muestras de test:", int(test.sum()), "| le ganan de verdad:", int(y[test].sum()))
    print(res.to_string(index=False))

    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    res.to_csv(CARPETA_RESULTADOS / "baselines.csv", index=False)
    pd.concat(predicciones).to_csv(CARPETA_RESULTADOS / "predicciones_baselines.csv", index=False)
