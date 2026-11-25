"""Extra, walk forward: en vez de un solo corte, probamos en 5 bloques de años que avanzan en el tiempo.
Extendido entrena con todo lo anterior a cada bloque. Rolling entrena solo con los últimos 5 años.
Mismas imágenes y misma red. Lo hacemos con las dos etiquetas, le gana y sube."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from baselines import variables
from config import (ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_RESULTADOS, HUECO_MINIMO,
                    WF_AÑOS_ROLLING, WF_BLOQUES, WF_FECHAS_VALIDACION)
from red import armar_red, cargar

CORRIDAS = 10
OBJETIVOS = {"le gana": ("etiqueta", ["rend_vs_spy", "volatilidad"]),
             "sube": ("sube", ["rend_20s", "volatilidad"])}
ESQUEMAS = ["extendido", "rolling"]
HUECO = pd.Timedelta(weeks=HUECO_MINIMO)


def cortes(fechas, inicio, fin, esquema):
    """Fechas de entrenamiento, validación y prueba para un bloque."""
    prueba = fechas[(fechas >= inicio) & (fechas <= fin)]
    hasta = inicio - HUECO  # así ninguna semana del entrenamiento se pisa con la prueba
    desde = hasta - pd.DateOffset(years=WF_AÑOS_ROLLING) if esquema == "rolling" else fechas.min()
    antes = fechas[(fechas >= desde) & (fechas <= hasta)]
    validacion = antes[-WF_FECHAS_VALIDACION:]
    entrena = antes[antes <= validacion.min() - HUECO]  # el mismo hueco entre entrenamiento y validación
    return entrena, validacion, prueba


if __name__ == "__main__":
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    precios = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])
    X, _ = cargar(m)  # las 2.600 imágenes, una sola vez
    num = variables(m, precios)
    fechas = pd.DatetimeIndex(sorted(m["fecha"].unique()))
    nombre = {b: f"{b[0][:4]}-{b[1][:4]}" for b in WF_BLOQUES}

    print("CÓMO QUEDAN LOS BLOQUES (imágenes para entrenar / validar / probar)")
    for esquema in ESQUEMAS:
        print(f"\n{esquema}")
        for b in WF_BLOQUES:
            tr, val, te = cortes(fechas, pd.Timestamp(b[0]), pd.Timestamp(b[1]), esquema)
            print(f"  prueba {nombre[b]}: entrena {tr.min().date()} a {tr.max().date()} | "
                  f"{m['fecha'].isin(tr).sum()} / {m['fecha'].isin(val).sum()} / {m['fecha'].isin(te).sum()}")

    filas, por_corrida = [], []
    for objetivo, (col, cols_log) in OBJETIVOS.items():
        y = m[col].to_numpy()
        for esquema in ESQUEMAS:
            for b in WF_BLOQUES:
                f_tr, f_val, f_te = cortes(fechas, pd.Timestamp(b[0]), pd.Timestamp(b[1]), esquema)
                tr, val, te = (m["fecha"].isin(f).to_numpy() for f in (f_tr, f_val, f_te))

                # baseline: la misma regresión logística de antes, con las mismas fechas
                log = make_pipeline(StandardScaler(), LogisticRegression())
                log.fit(num[cols_log].to_numpy()[tr], y[tr])
                auc_log = roc_auc_score(y[te], log.predict_proba(num[cols_log].to_numpy()[te])[:, 1])

                res = []
                for semilla in range(CORRIDAS):
                    tf.keras.backend.clear_session()
                    tf.keras.utils.set_random_seed(semilla)
                    red = armar_red()
                    red.compile(optimizer="adam", loss="binary_crossentropy")
                    freno = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
                    red.fit(X[tr], y[tr], validation_data=(X[val], y[val]), epochs=40, batch_size=32,
                            callbacks=[freno], verbose=0)
                    prob = red.predict(X[te], verbose=0).ravel()
                    pred = (prob > 0.5).astype(int)
                    res.append({"objetivo": objetivo, "esquema": esquema, "bloque": nombre[b], "semilla": semilla,
                                "auc": roc_auc_score(y[te], prob),
                                "precision": precision_score(y[te], pred, zero_division=np.nan),  # si no dice que sí nunca, queda vacía
                                "dice_positivo_%": pred.mean() * 100})
                res = pd.DataFrame(res)
                por_corrida.append(res)
                filas.append({"objetivo": objetivo, "esquema": esquema, "bloque": nombre[b],
                              "entrena": int(tr.sum()), "prueba": int(te.sum()),
                              "positivos_en_prueba_%": round(y[te].mean() * 100, 1),
                              "auc_logistica": round(auc_log, 3),
                              "auc_red": round(res["auc"].mean(), 3),
                              "auc_red_min": round(res["auc"].min(), 3),
                              "auc_red_max": round(res["auc"].max(), 3),
                              "corridas_auc_mayor_0,5": int((res["auc"] > 0.5).sum()),
                              "precision_red": round(res["precision"].mean(), 3),
                              "red_dice_positivo_%": round(res["dice_positivo_%"].mean(), 1)})
                print(f"{objetivo} | {esquema} | prueba {nombre[b]} listo")

    t = pd.DataFrame(filas)
    t.to_csv(CARPETA_RESULTADOS / "walk_forward.csv", index=False)
    pd.concat(por_corrida).to_csv(CARPETA_RESULTADOS / "walk_forward_corridas.csv", index=False)

    print("\nRESULTADOS POR BLOQUE (la red es el promedio de 10 corridas)")
    print("positivos_en_prueba_% es cuántas le ganan o suben de verdad, y también la precisión de decir siempre que sí")
    for objetivo in OBJETIVOS:
        print(f"\n{objetivo.upper()}")
        print(t[t["objetivo"] == objetivo].drop(columns="objetivo").to_string(index=False))

    print("\nPROMEDIO DE LOS 5 BLOQUES")
    resumen = t.groupby(["objetivo", "esquema"]).agg(
        auc_red=("auc_red", "mean"), auc_logistica=("auc_logistica", "mean"),
        bloques_red_mayor_0_5=("auc_red", lambda x: int((x > 0.5).sum())),
        precision_red=("precision_red", "mean"), positivos_en_prueba=("positivos_en_prueba_%", "mean"))
    resumen["bloques_red_mejor_que_logistica"] = (t.assign(gana=t["auc_red"] > t["auc_logistica"])
                                                  .groupby(["objetivo", "esquema"])["gana"].sum())
    print(resumen.round(3).to_string())
    print("\npara comparar, con el corte único de antes la red daba AUC 0,474 en le gana y 0,444 en sube")

    # gráfico: cuánto se aleja el AUC de 0,5 (tirar una moneda) en cada bloque
    fig, axes = plt.subplots(1, 2, figsize=(13, 4), sharey=True)
    bloques = [nombre[b] for b in WF_BLOQUES]
    x = np.arange(len(bloques))
    barras = [("extendido", "auc_red", "red extendido", "tab:blue"),
              ("rolling", "auc_red", "red rolling", "tab:orange"),
              ("extendido", "auc_logistica", "logística extendido", "lightsteelblue"),
              ("rolling", "auc_logistica", "logística rolling", "navajowhite")]
    for ax, objetivo in zip(axes, OBJETIVOS):
        for k, (esquema, col, etiqueta, color) in enumerate(barras):
            v = t[(t["objetivo"] == objetivo) & (t["esquema"] == esquema)].set_index("bloque").loc[bloques, col]
            ax.bar(x + (k - 1.5) * 0.2, v - 0.5, 0.2, bottom=0.5, label=etiqueta, color=color)
        ax.axhline(0.5, color="black", linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels([f"prueba {b}" for b in bloques], fontsize=8)
        ax.set_title(f"{objetivo}: AUC en cada bloque (0,5 es tirar una moneda)", fontsize=10)
    axes[0].set_ylabel("AUC")
    axes[0].set_ylim(0.3, 0.7)
    axes[0].legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(CARPETA_RESULTADOS / "walk_forward.png", dpi=120)
    print("\ngráfico guardado en resultados/walk_forward.png")
