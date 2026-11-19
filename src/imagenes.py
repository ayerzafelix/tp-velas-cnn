"""Dibuja una imagen de 20 velas por muestra y la guarda en data/imagenes/conjunto/clase/."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from config import (ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_IMAGENES, CARPETA_RESULTADOS,
                    LADO, VENTANA)

VERDE = (0, 200, 0)
ROJO = (220, 0, 0)


def dibujar(velas):
    """velas: tabla con open, high, low, close de 20 semanas. Devuelve una imagen de 64 x 64."""
    v = np.log(velas[["open", "high", "low", "close"]].to_numpy())
    piso, techo = v[:, 2].min(), v[:, 1].max()
    # paso cada precio a una fila de la imagen: el máximo de la ventana arriba y el mínimo abajo
    fila = lambda x: np.round((techo - x) / (techo - piso) * (LADO - 1)).astype(int)

    img = np.zeros((LADO, LADO, 3), dtype=np.uint8)
    for k, (o, h, l, c) in enumerate(v):
        color = VERDE if c >= o else ROJO
        x = 2 + 3 * k                      # cada vela ocupa 3 píxeles de ancho
        img[fila(h):fila(l) + 1, x + 1] = color                       # mecha
        arriba, abajo = sorted([fila(o), fila(c)])
        img[arriba:abajo + 1, x:x + 3] = color                        # cuerpo
    return img


if __name__ == "__main__":
    p = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"]).sort_values(["ticker", "fecha"])
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    por_ticker = {t: g.set_index("fecha") for t, g in p.groupby("ticker")}

    ejemplos = []
    for _, r in m.iterrows():
        serie = por_ticker[r["ticker"]]
        velas = serie.loc[:r["fecha"]].tail(VENTANA)
        # la última vela tiene que ser la de la semana t
        assert len(velas) == VENTANA and velas.index[-1] == r["fecha"]
        img = dibujar(velas)
        carpeta = CARPETA_IMAGENES / r["conjunto"] / str(r["etiqueta"])
        carpeta.mkdir(parents=True, exist_ok=True)
        Image.fromarray(img).save(carpeta / f"{r['ticker']}_{r['fecha'].date()}.png")
        if len(ejemplos) < 12 and r["conjunto"] == "train" and _ % 37 == 0:
            ejemplos.append((img, r["ticker"], r["fecha"].date(), r["etiqueta"]))

    total = sum(1 for _ in CARPETA_IMAGENES.rglob("*.png"))
    print("imágenes guardadas:", total)
    for c in ["train", "validacion", "test"]:
        print(c, {k: len(list((CARPETA_IMAGENES / c / k).glob("*.png"))) for k in ["0", "1"]})

    # algunas imágenes para revisar a ojo
    fig, axes = plt.subplots(2, 6, figsize=(12, 4.6))
    for ax, (img, t, f, e) in zip(axes.ravel(), ejemplos):
        ax.imshow(img)
        ax.set_title(f"{t} {f}\netiqueta {e}", fontsize=8)
        ax.axis("off")
    fig.tight_layout()
    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    fig.savefig(CARPETA_RESULTADOS / "ejemplos_imagenes.png", dpi=120)
    print("ejemplos guardados en resultados/ejemplos_imagenes.png")
