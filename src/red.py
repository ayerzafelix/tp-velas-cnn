"""Primera red convolucional: mira la imagen de 20 velas y dice si la acción le gana al SPY."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
from sklearn.metrics import precision_score, roc_auc_score

from config import ARCHIVO_ETIQUETAS, CARPETA_IMAGENES, CARPETA_RESULTADOS, LADO

tf.keras.utils.set_random_seed(42)


def cargar(m):
    rutas = [CARPETA_IMAGENES / c / str(e) / f"{t}_{f.date()}.png"
             for c, e, t, f in zip(m["conjunto"], m["etiqueta"], m["ticker"], m["fecha"])]
    X = np.stack([np.asarray(Image.open(r)) for r in rutas]).astype("float32") / 255
    return X, m["etiqueta"].to_numpy()


def armar_red():
    return tf.keras.Sequential([
        tf.keras.layers.Input((LADO, LADO, 3)),
        tf.keras.layers.Conv2D(16, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])


if __name__ == "__main__":
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    datos = {c: m[m["conjunto"] == c] for c in ["train", "validacion", "test"]}
    X_tr, y_tr = cargar(datos["train"])
    X_val, y_val = cargar(datos["validacion"])
    X_te, y_te = cargar(datos["test"])

    red = armar_red()
    red.compile(optimizer="adam", loss="binary_crossentropy", metrics=[tf.keras.metrics.AUC(name="auc")])
    # frena cuando la pérdida de validación deja de mejorar y se queda con la mejor época
    freno = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
    hist = red.fit(X_tr, y_tr, validation_data=(X_val, y_val), epochs=40, batch_size=32,
                   callbacks=[freno], verbose=2)

    prob = red.predict(X_te, verbose=0).ravel()
    pred = (prob > 0.5).astype(int)
    print("\népocas entrenadas:", len(hist.history["loss"]), "| mejor época:", int(np.argmin(hist.history["val_loss"])) + 1)
    print("test | AUC:", round(roc_auc_score(y_te, prob), 3),
          "| precisión en le gana:", round(precision_score(y_te, pred, zero_division=0), 3),
          "| veces que dice le gana:", int(pred.sum()), "de", len(pred))

    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    datos["test"][["ticker", "fecha"]].assign(modelo="red convolucional", prob=prob).to_csv(
        CARPETA_RESULTADOS / "predicciones_red.csv", index=False)

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
    for a, (k, titulo) in zip(ax, [("loss", "pérdida"), ("auc", "AUC")]):
        a.plot(hist.history[k], label="entrenamiento")
        a.plot(hist.history["val_" + k], label="validación")
        a.set_title(titulo)
        a.set_xlabel("época")
    ax[0].legend()
    fig.tight_layout()
    fig.savefig(CARPETA_RESULTADOS / "curvas_red.png", dpi=120)
    print("curvas guardadas en resultados/curvas_red.png")
