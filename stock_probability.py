import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


def calculate_stock_probability(csv_file: str) -> dict[str, float | str]:
    # Leer el archivo CSV
    df = pd.read_csv(
        csv_file, dtype={"Date": str, "Open": float, "Close": float, "Volume": float}
    )

    # Convertir la columna Date a datetime
    df["Date"] = pd.to_datetime(df["Date"])
    # Ordenar por fecha para asegurar el análisis cronológico correcto
    df = df.sort_values("Date")

    # Calcular los cambios porcentuales diarios
    df["Price_Change"] = df["Close"].pct_change().replace([np.inf, -np.inf], np.nan)

    # Crear características adicionales
    df["Previous_Close"] = df["Close"].shift(1)
    df["Volume_Change"] = df["Volume"].pct_change().replace([np.inf, -np.inf], np.nan)
    df["Price_Direction"] = np.where(df["Price_Change"] > 0, 1, 0)

    # Eliminar filas con valores NaN
    df = df.dropna()

    if len(df) < 5:
        raise ValueError(
            f"Insuficientes datos en {csv_file}. Se requieren al menos 5 días de datos."
        )

    # Calcular probabilidades basadas en el histórico
    total_days = len(df)
    up_days = len(df[df["Price_Direction"] == 1])

    prob_up = up_days / total_days

    # Calcular tendencia reciente (últimos 5 días)
    recent_trend = df["Price_Direction"].tail(5).mean()

    # Ajustar probabilidades con la tendencia reciente
    final_prob_up = (prob_up * 0.7) + (recent_trend * 0.3)
    final_prob_down = 1 - final_prob_up

    # Obtener último precio
    last_price = df["Close"].iloc[-1]

    return {
        "probabilidad_subida": round(final_prob_up * 100, 2),
        "probabilidad_bajada": round(final_prob_down * 100, 2),
        "ultimo_precio": round(last_price, 2),
        "tendencia_reciente": "Alcista" if recent_trend > 0.5 else "Bajista",
    }


def generate_tendency_report(
    input_dir: str = "input/tickers_history", output_file: str = "input/tendency.md"
) -> None:
    # Crear directorio de salida si no existe
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    # Obtener lista de archivos CSV
    csv_files = Path(input_dir).glob("*.csv")

    # Generar reporte
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Análisis de Tendencias de Acciones\n\n")

        for csv_file in csv_files:
            ticker = csv_file.stem.replace("_values", "")
            resultado = calculate_stock_probability(str(csv_file))

            f.write(f"## {ticker}\n\n")
            f.write(f"- Último precio: ${resultado['ultimo_precio']}\n")
            f.write(f"- Probabilidad de subida: {resultado['probabilidad_subida']}%\n")
            f.write(f"- Probabilidad de bajada: {resultado['probabilidad_bajada']}%\n")
            f.write(f"- Tendencia reciente: {resultado['tendencia_reciente']}\n\n")


if __name__ == "__main__":
    generate_tendency_report()
    print("Reporte generado en input/tendency.md")
