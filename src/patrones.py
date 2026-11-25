"""Subpregunta 4: ¿qué patrones usa la red para decir que una acción sube, y acierta con ellos?
Usamos la opinión promedio de las 10 redes de sube.py sobre cada imagen de test."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from baselines import variables
from config import ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_RESULTADOS, VENTANA


def describir_velas(m, precios):
    """Cosas que se ven en cada imagen: hacia dónde venía, cómo es la última vela y si forma un patrón con nombre."""
    por_ticker = {t: g.set_index("fecha").sort_index() for t, g in precios.groupby("ticker")}
    filas = []
    for _, r in m.iterrows():
        v = por_ticker[r["ticker"]].loc[:r["fecha"]].tail(VENTANA)
        o, h, l, c = v["open"].to_numpy(), v["high"].to_numpy(), v["low"].to_numpy(), v["close"].to_numpy()
        tendencia = c[-1] / c[0] - 1
        cuerpo, rango = abs(c[-1] - o[-1]), h[-1] - l[-1]
        mecha_inf, mecha_sup = min(o[-1], c[-1]) - l[-1], h[-1] - max(o[-1], c[-1])
        venia_bajando = c[-2] < c[-6]  # las 4 semanas antes de la última vela

        # patrones del material de velas, mirando la última vela (y la anterior para la envolvente)
        if cuerpo <= 0.1 * rango:
            patron = "doji"
        elif mecha_inf >= 2 * cuerpo and mecha_sup <= cuerpo:
            patron = "martillo después de bajar" if venia_bajando else "martillo sin bajar antes"
        elif c[-1] > o[-1] and c[-2] < o[-2] and c[-1] >= o[-2] and o[-1] <= c[-2]:
            patron = "envolvente alcista"
        elif c[-1] < o[-1] and c[-2] > o[-2] and c[-1] <= o[-2] and o[-1] >= c[-2]:
            patron = "envolvente bajista"
        else:
            patron = "ninguno"

        if tendencia < -0.10:
            tramo = "1. bajó más de 10%"
        elif tendencia < 0:
            tramo = "2. bajó hasta 10%"
        elif tendencia < 0.10:
            tramo = "3. subió hasta 10%"
        else:
            tramo = "4. subió más de 10%"
        filas.append({"tendencia_20s": tramo, "ultima_vela": "verde" if c[-1] >= o[-1] else "roja",
                      "patron_ultima_vela": patron})
    return pd.DataFrame(filas, index=m.index)


def tabla(d, columna, train):
    t = d.groupby(columna).agg(muestras=("sube", "size"),
                               red_dice_sube=("dice_sube", "mean"),
                               sube_de_verdad=("sube", "mean"),
                               acierta=("acierta", "mean"))
    if columna != "año":  # los años de test no están en train
        t["subia_en_train"] = train.groupby(columna)["sube"].mean()
    for col in [c for c in ["red_dice_sube", "sube_de_verdad", "acierta", "subia_en_train"] if c in t]:
        t[col] = (t[col] * 100).round(1)
    return t


if __name__ == "__main__":
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    precios = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])
    m = m.join(describir_velas(m, precios))
    vol = variables(m, precios)["volatilidad"]
    m["volatilidad"] = pd.qcut(vol, 3, labels=["1. baja", "2. media", "3. alta"])
    m["año"] = m["fecha"].dt.year

    p = pd.read_csv(CARPETA_RESULTADOS / "predicciones_sube_10.csv", parse_dates=["fecha"])
    prob = p.groupby(["ticker", "fecha"])["prob"].mean().rename("prob_promedio").reset_index()
    test = m[m["conjunto"] == "test"].merge(prob, on=["ticker", "fecha"])
    test["dice_sube"] = (test["prob_promedio"] > 0.5).astype(int)
    test["acierta"] = (test["dice_sube"] == test["sube"]).astype(int)
    train = m[m["conjunto"] == "train"]

    print("Usamos la opinión promedio de las 10 redes sobre cada imagen de test.")
    print(f"dice sube en {test['dice_sube'].mean():.1%} de los casos, sube de verdad el {test['sube'].mean():.1%}, acierta el {test['acierta'].mean():.1%}")
    print(f"su probabilidad va de {test['prob_promedio'].min():.2f} a {test['prob_promedio'].max():.2f}")
    print("\nlas columnas están en %: cuántas veces la red dice sube, cuántas sube de verdad, cuántas acierta,")
    print("y cuántas subían en entrenamiento con esa misma característica (lo que la red pudo aprender)")

    tablas = {}
    for titulo, col in [("HACIA DÓNDE VENÍA EN LAS 20 SEMANAS", "tendencia_20s"),
                        ("COLOR DE LA ÚLTIMA VELA", "ultima_vela"),
                        ("PATRÓN DE LA ÚLTIMA VELA (del material de velas)", "patron_ultima_vela"),
                        ("VOLATILIDAD DE LAS 20 SEMANAS", "volatilidad"),
                        ("SECTOR", "sector"),
                        ("AÑO", "año")]:
        tablas[col] = tabla(test, col, train)
        print(f"\n{titulo}")
        print(tablas[col].to_string())

    pd.concat({k: v.reset_index().rename(columns={k: "grupo"}) for k, v in tablas.items()}).to_csv(
        CARPETA_RESULTADOS / "patrones.csv")

    # gráfico: lo que dice la red contra lo que pasó, por tendencia y por patrón
    fig, axes = plt.subplots(1, 2, figsize=(13, 4))
    for ax, col, titulo in [(axes[0], "tendencia_20s", "según hacia dónde venía"),
                            (axes[1], "patron_ultima_vela", "según el patrón de la última vela")]:
        t = tablas[col]
        x = np.arange(len(t))
        ax.bar(x - 0.2, t["red_dice_sube"], 0.4, label="la red dice que sube", color="tab:orange")
        ax.bar(x + 0.2, t["sube_de_verdad"], 0.4, label="sube de verdad", color="tab:blue")
        ax.set_xticks(x)
        ax.set_xticklabels(t.index, rotation=25, ha="right", fontsize=8)
        ax.set_ylabel("% de las muestras de test")
        ax.set_title(titulo)
        ax.axhline(50, color="black", linewidth=0.6, linestyle="--")
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(CARPETA_RESULTADOS / "patrones.png", dpi=120)
    print("\ngráfico guardado en resultados/patrones.png")
