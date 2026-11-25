"""Más análisis exploratorio: cuánto se mueve una acción en 8 semanas y cuánto se mueven juntas las 50."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import ACCIONES, ARCHIVO_ETIQUETAS, ARCHIVO_PRECIOS, CARPETA_RESULTADOS, REFERENCIA, SECTORES

ORDEN = ["train", "validacion", "test"]
COLORES = {"train": "tab:blue", "validacion": "tab:orange", "test": "tab:green"}

if __name__ == "__main__":
    m = pd.read_csv(ARCHIVO_ETIQUETAS, parse_dates=["fecha"])
    precios = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])
    CARPETA_RESULTADOS.mkdir(exist_ok=True)

    # 1. lo binario esconde cuánto se movió, como marcó Pedro
    m["sola_%"] = (np.exp(m["rend_absoluto"]) - 1) * 100
    m["vs_spy_%"] = (np.exp(m["rend_relativo"]) - 1) * 100
    print("1. CUÁNTO SE MUEVE UNA ACCIÓN EN LAS 8 SEMANAS SIGUIENTES, en %")
    filas = []
    for col, nombre in [("sola_%", "la acción sola"), ("vs_spy_%", "la acción contra el SPY")]:
        x = m[col]
        filas.append({"": nombre, "promedio": x.mean(), "mediana": x.median(), "desvío": x.std(),
                      "peor 10%": x.quantile(0.1), "mejor 10%": x.quantile(0.9),
                      "% que se movió menos de 2%": (x.abs() < 2).mean() * 100})
    print(pd.DataFrame(filas).set_index("").round(1).to_string())

    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5), sharey=True)
    for ax, col, titulo in [(axes[0], "sola_%", "la acción sola (etiqueta sube)"),
                            (axes[1], "vs_spy_%", "la acción contra el SPY (etiqueta le gana)")]:
        ax.hist(m[col].clip(-40, 40), bins=40, color="tab:blue")
        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_title(titulo)
        ax.set_xlabel("% en las 8 semanas siguientes (cortado en 40%)")
    axes[0].set_ylabel("muestras")
    fig.tight_layout()
    fig.savefig(CARPETA_RESULTADOS / "exploratorio_rendimientos.png", dpi=120)

    # 2. en cada fecha, cuántas de las 50 suben. Gabi marcó que se mueven juntas con el mercado
    por_fecha = m.groupby("fecha").agg(conjunto=("conjunto", "first"), sube=("sube", "mean"),
                                       le_gana=("etiqueta", "mean"))
    por_fecha[["sube", "le_gana"]] *= 100
    n = len(ACCIONES)
    print(f"\n2. ¿SE MUEVEN JUNTAS? {len(por_fecha)} fechas, {n} acciones en cada una")
    print("si cada acción se moviera por su lado (como tirar 50 monedas), el % de cada fecha caería casi siempre en el rango de abajo")
    rangos = {}
    for col, nombre in [("sube", "suben"), ("le_gana", "le ganan al SPY")]:
        p = por_fecha[col].mean() / 100
        margen = 2 * np.sqrt(p * (1 - p) / n) * 100
        rangos[col] = (p * 100 - margen, p * 100 + margen)
        fuera = ((por_fecha[col] - p * 100).abs() > margen).mean()
        print(f"\n{nombre}: en promedio {p:.1%}, rango si fueran por su lado {rangos[col][0]:.0f}% a {rangos[col][1]:.0f}%")
        print(f"  fechas fuera de ese rango: {fuera:.0%}")
        print(f"  la peor fecha {por_fecha[col].min():.0f}% ({por_fecha[col].idxmin().date()}), "
              f"la mejor {por_fecha[col].max():.0f}% ({por_fecha[col].idxmax().date()})")
    print("\ncuánto cambia el % de una fecha a otra (desvío), por conjunto")
    print(por_fecha.groupby("conjunto")[["sube", "le_gana"]].std().reindex(ORDEN).round(1).to_string())
    por_fecha.round(1).to_csv(CARPETA_RESULTADOS / "exploratorio_por_fecha.csv")

    fig, axes = plt.subplots(2, 1, figsize=(11, 5.5), sharex=True)
    for ax, col, titulo in [(axes[0], "sube", "% de las 50 que sube"),
                            (axes[1], "le_gana", "% de las 50 que le gana al SPY")]:
        ax.bar(por_fecha.index, por_fecha[col], width=100, color=[COLORES[c] for c in por_fecha["conjunto"]])
        ax.axhspan(*rangos[col], color="gray", alpha=0.3, label="rango si cada una fuera por su lado")
        ax.set_ylim(0, 100)
        ax.set_ylabel("%")
        ax.set_title(f"{titulo} en cada fecha (azul train, naranja validación, verde test)", fontsize=9)
    axes[0].legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    fig.savefig(CARPETA_RESULTADOS / "exploratorio_por_fecha.png", dpi=120)

    # 3. correlación de los rendimientos semanales, en promedio por par de sectores
    cierres = precios.pivot(index="fecha", columns="ticker", values="close")
    rend = np.log(cierres).diff().dropna()
    corr = rend[ACCIONES].corr()
    sector_de = {t: s for s, lista in SECTORES.items() for t in lista}
    mismo, distinto = [], []
    for i, a in enumerate(ACCIONES):
        for b in ACCIONES[i + 1:]:
            (mismo if sector_de[a] == sector_de[b] else distinto).append(corr.loc[a, b])
    con_spy = rend[ACCIONES].corrwith(rend[REFERENCIA])
    print("\n3. CORRELACIÓN DE LOS RENDIMIENTOS SEMANALES (0 no tienen nada que ver, 1 se mueven igual)")
    print(f"dos acciones del mismo sector: {np.mean(mismo):.2f}")
    print(f"dos acciones de sectores distintos: {np.mean(distinto):.2f}")
    print(f"cada acción con el SPY: {con_spy.mean():.2f} (de {con_spy.min():.2f} en {con_spy.idxmin()} a {con_spy.max():.2f} en {con_spy.idxmax()})")

    nombres = list(SECTORES)
    tabla = pd.DataFrame(index=nombres, columns=nombres, dtype=float)
    for s1 in nombres:
        for s2 in nombres:
            valores = [corr.loc[a, b] for a in SECTORES[s1] for b in SECTORES[s2] if a != b]
            tabla.loc[s1, s2] = np.mean(valores)
    tabla.round(2).to_csv(CARPETA_RESULTADOS / "exploratorio_correlacion.csv")

    fig, ax = plt.subplots(figsize=(7.5, 6))
    im = ax.imshow(tabla.to_numpy(), cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(nombres)))
    ax.set_yticklabels(nombres, fontsize=8)
    for i in range(len(nombres)):
        for j in range(len(nombres)):
            v = tabla.iloc[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7, color="white" if v > 0.6 else "black")
    ax.set_title("correlación promedio de los rendimientos semanales entre sectores", fontsize=9)
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(CARPETA_RESULTADOS / "exploratorio_correlacion.png", dpi=120)
    print("\ngráficos guardados en resultados/exploratorio_rendimientos.png, exploratorio_por_fecha.png y exploratorio_correlacion.png")
