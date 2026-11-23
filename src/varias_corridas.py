"""Entrena la misma red 10 veces con semillas distintas para ver cuánto cambia el resultado por azar."""
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import precision_score, roc_auc_score

from backtest import simular
from config import ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_RESULTADOS
from red import armar_red, cargar

CORRIDAS = 10

if __name__ == "__main__":
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    datos = {c: m[m["conjunto"] == c] for c in ["train", "validacion", "test"]}
    X_tr, y_tr = cargar(datos["train"])
    X_val, y_val = cargar(datos["validacion"])
    X_te, y_te = cargar(datos["test"])
    precios = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])
    cierres = precios.pivot(index="fecha", columns="ticker", values="close").sort_index()

    filas, todas = [], []
    for semilla in range(CORRIDAS):
        tf.keras.utils.set_random_seed(semilla)
        red = armar_red()
        red.compile(optimizer="adam", loss="binary_crossentropy")
        freno = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
        red.fit(X_tr, y_tr, validation_data=(X_val, y_val), epochs=40, batch_size=32,
                callbacks=[freno], verbose=0)

        prob = red.predict(X_te, verbose=0).ravel()
        pred = (prob > 0.5).astype(int)
        todas.append(datos["test"][["ticker", "sector", "fecha", "etiqueta", "rend_relativo"]].assign(semilla=semilla, prob=prob))
        rend, compras = simular(datos["test"][["ticker", "fecha"]].assign(prob=prob), cierres)
        filas.append({"semilla": semilla,
                      "auc": roc_auc_score(y_te, prob),
                      "precision_le_gana": precision_score(y_te, pred, zero_division=0),
                      "compras": compras,
                      "backtest_%": rend * 100})
        print(f"corrida {semilla + 1} de {CORRIDAS} lista")

    res = pd.DataFrame(filas)
    print("\n" + res.round(3).to_string(index=False))

    resumen = res.drop(columns="semilla").agg(["mean", "min", "max"]).T
    resumen.columns = ["promedio", "mínimo", "máximo"]
    print("\nresumen de las", CORRIDAS, "corridas")
    print(resumen.round(3).to_string())

    # la vara: decir siempre "le gana" y comprar SPY
    base = pd.read_csv(CARPETA_RESULTADOS / "baselines.csv").set_index("modelo")
    bt = pd.read_csv(CARPETA_RESULTADOS / "backtest.csv").set_index("estrategia")["rendimiento_acumulado"]
    vara = base.loc["siempre la clase más frecuente", "precision_le_gana_test"]
    print(f"\npara comparar: siempre decir le gana da precisión {vara:.3f} y backtest {bt['siempre la clase más frecuente']:.1f}%, SPY {bt['comprar SPY']:.1f}%")
    print("corridas con precisión mayor a", f"{vara:.3f}:", int((res["precision_le_gana"] > vara).sum()), "de", CORRIDAS)
    print("corridas con AUC mayor a 0,5:", int((res["auc"] > 0.5).sum()), "de", CORRIDAS)
    print("corridas con backtest mayor al de SPY:", int((res["backtest_%"] > bt["comprar SPY"]).sum()), "de", CORRIDAS)

    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    res.to_csv(CARPETA_RESULTADOS / "red_varias_corridas.csv", index=False)
    # las predicciones de cada corrida, para analizarlas después
    pd.concat(todas).to_csv(CARPETA_RESULTADOS / "predicciones_red_10.csv", index=False)
