"""Revisa que los precios tengan sentido antes de usarlos."""
import pandas as pd

from config import ARCHIVO_PRECIOS, CARPETA_RESULTADOS

if __name__ == "__main__":
    p = pd.read_csv(ARCHIVO_PRECIOS, parse_dates=["fecha"]).sort_values(["ticker", "fecha"])

    # dejo un margen chico porque el ajuste por dividendos redondea los precios
    mal_high = (p["high"] < p[["open", "close"]].max(axis=1) * 0.999).sum()
    mal_low = (p["low"] > p[["open", "close"]].min(axis=1) * 1.001).sum()
    print("velas con el máximo mal:", mal_high)
    print("velas con el mínimo mal:", mal_low)
    print("precios en cero o negativos:", (p[["open", "high", "low", "close"]] <= 0).sum().sum())

    # semanas donde el cierre se movió más de 40%
    p["var_semanal"] = p.groupby("ticker")["close"].pct_change()
    saltos = p[p["var_semanal"].abs() > 0.4][["ticker", "sector", "fecha", "var_semanal"]]
    saltos = saltos.sort_values("var_semanal")
    print("semanas con saltos de más de 40%:", len(saltos))
    print(saltos.to_string(index=False))

    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    saltos.to_csv(CARPETA_RESULTADOS / "saltos_semanales.csv", index=False)
