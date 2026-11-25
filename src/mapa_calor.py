"""Grad-CAM: qué parte de la imagen mira la red para decidir."""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

from config import ARCHIVO_ETIQUETAS, CARPETA_RESULTADOS, LADO, VENTANA
from red import cargar


def modelo_con_conv(red):
    """Arma la misma red pero devolviendo también la salida de la última capa convolucional."""
    ultima = max(i for i, capa in enumerate(red.layers) if isinstance(capa, tf.keras.layers.Conv2D))
    entrada = tf.keras.Input((LADO, LADO, 3))
    x = entrada
    for i, capa in enumerate(red.layers):
        x = capa(x)
        if i == ultima:
            conv = x
    return tf.keras.Model(entrada, [conv, x])


def grad_cam(modelo, img):
    """Mapa de lo que empuja a la red hacia la clase que eligió para esa imagen."""
    with tf.GradientTape() as tape:
        conv, pred = modelo(img[None])
        # si dice "le gana" miro qué empuja hacia arriba la probabilidad, si dice "no" qué la empuja hacia abajo
        salida = pred[:, 0] if pred[0, 0] > 0.5 else 1 - pred[:, 0]
    grads = tape.gradient(salida, conv)
    # cada filtro pesa según cuánto cambia la salida cuando cambia ese filtro
    pesos = tf.reduce_mean(grads, axis=(0, 1, 2))
    mapa = tf.nn.relu(tf.reduce_sum(conv[0] * pesos, axis=-1))
    mapa = tf.image.resize(mapa[..., None], (LADO, LADO))[..., 0].numpy()
    return mapa / (mapa.max() + 1e-8), float(pred[0, 0])


if __name__ == "__main__":
    # "python src/mapa_calor.py sube" usa la red que predice si la acción sube
    sube = len(sys.argv) > 1 and sys.argv[1] == "sube"
    columna, fin = ("sube", "_sube") if sube else ("etiqueta", "")
    red = tf.keras.models.load_model(CARPETA_RESULTADOS / f"red{fin}.keras")
    modelo = modelo_con_conv(red)
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    test = m[m["conjunto"] == "test"].reset_index(drop=True)
    X, y = cargar(test, columna)

    mapas, probs = zip(*[grad_cam(modelo, x) for x in X])
    mapas, probs = np.stack(mapas), np.array(probs)

    # cuánto mira cada una de las 20 velas en promedio (cada vela ocupa 3 columnas desde la columna 2)
    por_columna = mapas.mean(axis=(0, 1))
    por_vela = np.array([por_columna[2 + 3 * k: 5 + 3 * k].mean() for k in range(VENTANA)])
    por_vela = por_vela / por_vela.sum() * 100
    print("cuánto mira la red cada vela, en % del total (vela 1 es la más vieja, vela 20 la semana t)")
    for k, v in enumerate(por_vela, start=1):
        print(f"vela {k:2d}: {v:4.1f}% " + "#" * int(round(v)))
    print(f"\nlas últimas 5 velas se llevan el {por_vela[-5:].sum():.1f}% de la atención (serían 25% si mirara todo parejo)")

    # ejemplos: las 3 imágenes donde la red está más segura de "le gana" y las 3 de "no le gana"
    orden = np.argsort(probs)
    elegidas = list(orden[-3:][::-1]) + list(orden[:3])
    fig, axes = plt.subplots(2, 6, figsize=(14, 5))
    for col, i in enumerate(elegidas):
        r = test.iloc[i]
        titulo = f"{r['ticker']} {r['fecha'].date()}\nprob {probs[i]:.2f} | real {r[columna]}"
        axes[0, col].imshow(X[i])
        axes[0, col].set_title(titulo, fontsize=8)
        axes[1, col].imshow(X[i])
        axes[1, col].imshow(mapas[i], cmap="jet", alpha=0.45)
        for a in axes[:, col]:
            a.axis("off")
    clase = "sube" if sube else "le gana"
    fig.suptitle(f"arriba la imagen, abajo dónde mira la red para decidir. Izquierda: más segura de que {clase}. Derecha: más segura de que no", fontsize=9)
    fig.tight_layout()
    fig.savefig(CARPETA_RESULTADOS / f"mapa_calor_ejemplos{fin}.png", dpi=120)

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.bar(range(1, VENTANA + 1), por_vela, color="tab:orange")
    ax.axhline(100 / VENTANA, color="black", linewidth=0.8, linestyle="--", label="si mirara todas parejo")
    ax.set_xlabel("vela (1 = la más vieja, 20 = la semana t)")
    ax.set_ylabel("% de la atención")
    ax.set_xticks(range(1, VENTANA + 1))
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(CARPETA_RESULTADOS / f"mapa_calor_por_vela{fin}.png", dpi=120)
    print(f"gráficos guardados en resultados/mapa_calor_ejemplos{fin}.png y resultados/mapa_calor_por_vela{fin}.png")
