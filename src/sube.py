"""Subpregunta 3: sin compararla con el SPY, ¿la red puede anticipar si la acción sube en las 8 semanas siguientes?
Mismas imágenes, mismo split y misma red. Lo único que cambia es la etiqueta."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from baselines import variables
from config import ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_RESULTADOS
from red import armar_red, cargar

CORRIDAS = 10
ORDEN = ["train", "validacion", "test"]

if __name__ == "__main__":
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    precios = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])

    # 1. la etiqueta nueva: cuántas veces sube
    print("1. ¿CUÁNTAS VECES SUBE UNA ACCIÓN EN 8 SEMANAS?")
    print(f"total: {m['sube'].mean():.1%} de {len(m)} muestras")
    print("\npor conjunto")
    print((m.groupby("conjunto")["sube"].mean() * 100).reindex(ORDEN).round(1).rename("% que sube").to_string())
    print("\npor sector")
    print((m.groupby("sector")["sube"].mean() * 100).sort_values().round(1).rename("% que sube").to_string())
    m["año"] = m["fecha"].dt.year
    por_anio = m.groupby("año")["sube"].mean() * 100

    fig, ax = plt.subplots(figsize=(10, 3.5))
    colores = {"train": "tab:blue", "validacion": "tab:orange", "test": "tab:green"}
    conj_anio = m.groupby("año")["conjunto"].agg(lambda x: x.mode()[0])
    ax.bar(por_anio.index, por_anio.values, color=[colores[conj_anio[a]] for a in por_anio.index])
    ax.axhline(50, color="black", linewidth=0.8, linestyle="--")
    ax.set_ylabel("% de muestras que sube")
    ax.set_title("cuántas acciones suben en las 8 semanas siguientes, por año (azul train, naranja validación, verde test)")
    fig.tight_layout()
    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    fig.savefig(CARPETA_RESULTADOS / "sube_por_anio.png", dpi=120)

    # 2. baselines con la etiqueta nueva
    X_num = variables(m, precios)[["rend_20s", "volatilidad"]]
    y = m["sube"]
    train, test = m["conjunto"] == "train", m["conjunto"] == "test"
    print("\n2. BASELINES EN TEST")
    filas = []
    for nombre, modelo in {
        "siempre la clase más frecuente": DummyClassifier(strategy="most_frequent"),
        "regresión logística (rendimiento de las 20 semanas y volatilidad)": make_pipeline(StandardScaler(), LogisticRegression()),
    }.items():
        modelo.fit(X_num[train], y[train])
        prob = modelo.predict_proba(X_num[test])[:, 1]
        pred = (prob > 0.5).astype(int)
        filas.append({"modelo": nombre, "auc": round(roc_auc_score(y[test], prob), 3),
                      "precision_sube": round(precision_score(y[test], pred, zero_division=0), 3),
                      "veces_que_dice_sube": int(pred.sum())})
    base = pd.DataFrame(filas)
    print(f"muestras de test: {int(test.sum())} | suben de verdad: {int(y[test].sum())}")
    print(base.to_string(index=False))
    base.to_csv(CARPETA_RESULTADOS / "sube_baselines.csv", index=False)

    # 3. la misma red, 10 corridas, ahora prediciendo si sube
    datos = {c: m[m["conjunto"] == c] for c in ORDEN}
    X_tr, y_tr = cargar(datos["train"], "sube")
    X_val, y_val = cargar(datos["validacion"], "sube")
    X_te, y_te = cargar(datos["test"], "sube")

    res, todas = [], []
    for semilla in range(CORRIDAS):
        tf.keras.utils.set_random_seed(semilla)
        red = armar_red()
        red.compile(optimizer="adam", loss="binary_crossentropy")
        freno = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
        hist = red.fit(X_tr, y_tr, validation_data=(X_val, y_val), epochs=40, batch_size=32,
                       callbacks=[freno], verbose=0)
        prob = red.predict(X_te, verbose=0).ravel()
        pred = (prob > 0.5).astype(int)
        res.append({"semilla": semilla, "mejor_época": int(np.argmin(hist.history["val_loss"])) + 1,
                    "auc": roc_auc_score(y_te, prob),
                    "precision_sube": precision_score(y_te, pred, zero_division=0),
                    "dice_sube": int(pred.sum())})
        todas.append(datos["test"][["ticker", "sector", "fecha", "sube", "rend_absoluto"]].assign(semilla=semilla, prob=prob))
        if semilla == 0:
            red.save(CARPETA_RESULTADOS / "red_sube.keras")  # la guardo para el mapa de calor
        print(f"corrida {semilla + 1} de {CORRIDAS} lista")

    res = pd.DataFrame(res)
    print("\n3. LA RED EN 10 CORRIDAS (test)")
    print(res.round(3).to_string(index=False))
    resumen = res.drop(columns="semilla").agg(["mean", "min", "max"]).T
    resumen.columns = ["promedio", "mínimo", "máximo"]
    print("\n" + resumen.round(3).to_string())

    vara = base.loc[0, "precision_sube"]
    print(f"\npara comparar: decir siempre sube da AUC 0,5 y precisión {vara:.3f}")
    print("corridas con AUC mayor a 0,5:", int((res["auc"] > 0.5).sum()), "de", CORRIDAS)
    print(f"corridas con precisión mayor a {vara:.3f}:", int((res["precision_sube"] > vara).sum()), "de", CORRIDAS)

    res.to_csv(CARPETA_RESULTADOS / "sube_10_corridas.csv", index=False)
    pd.concat(todas).to_csv(CARPETA_RESULTADOS / "predicciones_sube_10.csv", index=False)
