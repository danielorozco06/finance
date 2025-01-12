import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


def calculate_stock_probability(csv_file: str) -> dict[str, float | str]:
    # Verificar que el archivo existe
    if not Path(csv_file).exists():
        raise FileNotFoundError(f"No se encontró el archivo: {csv_file}")

    # Leer el archivo CSV
    try:
        df = pd.read_csv(
            csv_file,
            dtype={"Date": str, "Open": float, "Close": float, "Volume": float},
        )
    except Exception as e:
        raise ValueError(f"Error al leer el archivo {csv_file}: {str(e)}")

    # Verificar columnas requeridas
    required_columns = {"Date", "Close", "Volume"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Columnas faltantes en {csv_file}. Se requieren: {required_columns}"
        )

    # Convertir la columna Date a datetime
    df["Date"] = pd.to_datetime(df["Date"])
    # Ordenar por fecha para asegurar el análisis cronológico correcto
    df = df.sort_values("Date")

    # Verificar que hay suficientes datos
    if len(df) < 120:  # Aproximadamente 6 meses de datos (20 días * 6)
        raise ValueError(
            f"Insuficientes datos en {csv_file}. Se requieren al menos 120 días de datos."
        )

    # Calcular los cambios porcentuales diarios
    df["Price_Change"] = df["Close"].pct_change().replace([np.inf, -np.inf], np.nan)
    df["Price_Direction"] = np.where(df["Price_Change"] > 0, 1, 0)

    def calculate_trend(days: int) -> tuple[float, str]:
        # Usar los datos más recientes para predecir la tendencia futura
        recent_data = df["Price_Direction"].tail(min(days * 2, len(df)))
        trend_value = recent_data.mean()
        # Ajustar el mensaje para indicar predicción
        trend_direction = (
            "Probablemente Alcista" if trend_value > 0.5 else "Probablemente Bajista"
        )
        probability_up = round(trend_value * 100, 2)
        return probability_up, trend_direction

    # Eliminar filas con valores NaN
    df = df.dropna()

    if len(df) == 0:
        raise ValueError(f"No hay datos válidos después de procesar {csv_file}")

    # Calcular tendencias para diferentes períodos futuros
    prob_1d, trend_1d = calculate_trend(1)  # Próximo día
    prob_1w, trend_1w = calculate_trend(5)  # Próxima semana
    prob_3m, trend_3m = calculate_trend(60)  # Próximos 3 meses
    prob_6m, trend_6m = calculate_trend(120)  # Próximos 6 meses

    # Obtener último precio
    last_price = df["Close"].iloc[-1]

    return {
        "ultimo_precio": round(last_price, 2),
        "tendencia_prox_1d": trend_1d,
        "prob_subida_1d": prob_1d,
        "tendencia_prox_1s": trend_1w,
        "prob_subida_1s": prob_1w,
        "tendencia_prox_3m": trend_3m,
        "prob_subida_3m": prob_3m,
        "tendencia_prox_6m": trend_6m,
        "prob_subida_6m": prob_6m,
    }


def generate_tendency_report(
    input_dir: str = "input/tickers_history", output_file: str = "input/tendency.md"
) -> None:
    # Verificar que el directorio existe
    if not Path(input_dir).is_dir():
        raise NotADirectoryError(f"No se encontró el directorio: {input_dir}")

    # Crear directorio de salida si no existe
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    # Obtener lista de archivos CSV
    csv_files = list(Path(input_dir).glob("*.csv"))
    if not csv_files:
        raise ValueError(f"No se encontraron archivos CSV en {input_dir}")

    # Generar reporte
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Análisis de Tendencias de Acciones\n\n")

        for csv_file in csv_files:
            try:
                ticker = csv_file.stem.replace("_values", "")
                resultado = calculate_stock_probability(str(csv_file))

                f.write(f"## {ticker}\n\n")
                f.write(f"- Último precio: ${resultado['ultimo_precio']}\n")
                f.write("### Predicción de Tendencias\n")
                f.write(
                    f"- Próximo día: {resultado['tendencia_prox_1d']} (Prob. subida: {resultado['prob_subida_1d']}%)\n"
                )
                f.write(
                    f"- Próxima semana: {resultado['tendencia_prox_1s']} (Prob. subida: {resultado['prob_subida_1s']}%)\n"
                )
                f.write(
                    f"- Próximos 3 meses: {resultado['tendencia_prox_3m']} (Prob. subida: {resultado['prob_subida_3m']}%)\n"
                )
                f.write(
                    f"- Próximos 6 meses: {resultado['tendencia_prox_6m']} (Prob. subida: {resultado['prob_subida_6m']}%)\n\n"
                )
            except Exception as e:
                f.write(f"## {ticker}\n\n")
                f.write(f"Error al procesar: {str(e)}\n\n")


if __name__ == "__main__":
    generate_tendency_report()
    print("Reporte generado en input/tendency.md")
