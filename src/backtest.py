"""Simula invertir en test siguiendo a cada modelo y lo compara con comprar SPY en las mismas fechas."""
import numpy as np
import pandas as pd

from config import ARCHIVO_PRECIOS, CARPETA_RESULTADOS, HORIZONTE, REFERENCIA

COSTO = 0.001  # 0,1% por compra y por venta


def resultado_periodo(rendimientos, costo=COSTO):
    """Compra en partes iguales, mantiene 8 semanas y vende. Si no hay nada para comprar queda en efectivo."""
    if len(rendimientos) == 0:
        return 0.0
    return (1 - costo) * (1 + np.mean(rendimientos)) * (1 - costo) - 1


def acumulado(periodos):
    return np.prod([1 + r for r in periodos]) - 1


if __name__ == "__main__":
    # chequeo con un caso calculado a mano: dos acciones que suben 10% y 20%, costo 0,1%
    # 0,999 x 1,15 x 0,999 - 1 = 0,14770
    assert abs(resultado_periodo([0.10, 0.20]) - 0.14770) < 1e-4
    assert resultado_periodo([]) == 0.0
    assert abs(acumulado([0.10, -0.10]) - (-0.01)) < 1e-9

    precios = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"])
    cierres = precios.pivot(index="fecha", columns="ticker", values="close").sort_index()
    posicion = {f: i for i, f in enumerate(cierres.index)}

    def rendimiento(ticker, fecha):
        i = posicion[fecha]
        return cierres[ticker].iloc[i + HORIZONTE] / cierres[ticker].iloc[i] - 1

    archivos = [CARPETA_RESULTADOS / "predicciones_baselines.csv", CARPETA_RESULTADOS / "predicciones_red.csv"]
    preds = pd.concat([pd.read_csv(a, parse_dates=["fecha"]) for a in archivos if a.exists()])
    fechas = sorted(preds["fecha"].unique())

    spy = [resultado_periodo([rendimiento(REFERENCIA, f)]) for f in fechas]
    filas = [{"estrategia": "comprar SPY", "rendimiento_acumulado": acumulado(spy), "compras": len(fechas)}]
    for modelo, g in preds.groupby("modelo"):
        periodos, compradas = [], 0
        for f in fechas:
            elegidas = g[(g["fecha"] == f) & (g["prob"] > 0.5)]["ticker"]
            periodos.append(resultado_periodo([rendimiento(t, f) for t in elegidas]))
            compradas += len(elegidas)
        filas.append({"estrategia": modelo, "rendimiento_acumulado": acumulado(periodos), "compras": compradas})

    res = pd.DataFrame(filas)
    res["rendimiento_acumulado"] = (res["rendimiento_acumulado"] * 100).round(1)
    print(f"test: {len(fechas)} períodos de {HORIZONTE} semanas, desde {pd.Timestamp(fechas[0]).date()}, costo {COSTO:.1%} por operación")
    print(res.rename(columns={"rendimiento_acumulado": "rendimiento_acumulado_%"}).to_string(index=False))
    res.to_csv(CARPETA_RESULTADOS / "backtest.csv", index=False)

    # detalle de la red: de qué períodos y de qué acciones sale el resultado
    red = preds[preds["modelo"] == "red convolucional"]
    if len(red):
        detalle, aportes = [], []
        for f, r_spy in zip(fechas, spy):
            elegidas = red[(red["fecha"] == f) & (red["prob"] > 0.5)]["ticker"]
            rends = [rendimiento(t, f) for t in elegidas]
            detalle.append({"fecha": pd.Timestamp(f).date(), "compras": len(rends),
                            "red_%": round(resultado_periodo(rends) * 100, 1), "spy_%": round(r_spy * 100, 1)})
            # cada acción pesa lo mismo dentro del período
            aportes += [{"ticker": t, "fecha": pd.Timestamp(f).date(), "rendimiento_%": round(x * 100, 1),
                         "aporte_al_periodo_%": round(x / len(rends) * 100, 1)} for t, x in zip(elegidas, rends)]
        detalle, aportes = pd.DataFrame(detalle), pd.DataFrame(aportes)

        print("\nred convolucional, período por período")
        print(detalle.to_string(index=False))
        print("\nlas 5 compras que más aportaron")
        print(aportes.sort_values("aporte_al_periodo_%", ascending=False).head(5).to_string(index=False))
        detalle.to_csv(CARPETA_RESULTADOS / "backtest_red_por_periodo.csv", index=False)
        aportes.to_csv(CARPETA_RESULTADOS / "backtest_red_compras.csv", index=False)
