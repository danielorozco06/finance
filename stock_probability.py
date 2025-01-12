import warnings
from pathlib import Path

import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores técnicos avanzados para mejorar la predicción."""
    # Medias móviles
    df["SMA_5"] = df["Close"].rolling(window=5).mean()
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()

    # Volatilidad
    df["Volatility"] = df["Close"].rolling(window=20).std()

    # RSI
    delta = df["Close"].diff()
    delta = pd.to_numeric(delta, errors="coerce")
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Momentum
    df["Momentum"] = df["Close"] - df["Close"].shift(4)

    # Bollinger Bands
    df["BB_middle"] = df["Close"].rolling(window=20).mean()
    df["BB_upper"] = df["BB_middle"] + 2 * df["Close"].rolling(window=20).std()
    df["BB_lower"] = df["BB_middle"] - 2 * df["Close"].rolling(window=20).std()
    df["BB_width"] = (df["BB_upper"] - df["BB_lower"]) / df["BB_middle"]

    return df


def calculate_trend(df: pd.DataFrame, days: int) -> tuple[float, str]:
    """Calcula tendencia usando múltiples factores técnicos."""
    recent_df = df.tail(min(days * 3, len(df)))

    # Señales técnicas
    signals = []

    # 1. Tendencia de precio (comparación con medias móviles)
    price = recent_df["Close"].iloc[-1]
    sma_5 = recent_df["SMA_5"].iloc[-1]
    sma_20 = recent_df["SMA_20"].iloc[-1]
    sma_50 = recent_df["SMA_50"].iloc[-1]

    signals.append(1 if price > sma_5 else 0)
    signals.append(1 if price > sma_20 else 0)
    signals.append(1 if price > sma_50 else 0)

    # 2. RSI
    rsi = recent_df["RSI"].iloc[-1]
    signals.append(1 if 30 < rsi < 70 else 0)  # No sobrecomprado/sobrevendido

    # 3. Momentum
    momentum = recent_df["Momentum"].iloc[-1]
    signals.append(1 if momentum > 0 else 0)

    # 4. Volatilidad
    current_volatility = recent_df["Volatility"].iloc[-1]
    avg_volatility = recent_df["Volatility"].mean()
    signals.append(1 if current_volatility < avg_volatility else 0)

    # 5. Bandas de Bollinger
    bb_position = (price - recent_df["BB_lower"].iloc[-1]) / (
        recent_df["BB_upper"].iloc[-1] - recent_df["BB_lower"].iloc[-1]
    )
    signals.append(1 if 0.3 < bb_position < 0.7 else 0)

    # 6. Análisis estadístico
    returns = pd.to_numeric(recent_df["Close"], errors="coerce").pct_change().dropna()
    returns_array = pd.Series(returns).values
    t_stat, p_value = stats.ttest_1samp(returns_array, 0)
    signals.append(1 if float(t_stat) > 0 and float(p_value) < 0.05 else 0)

    # Calcular probabilidad
    prob_up = sum(signals) / len(signals) * 100

    # Determinar tendencia con más matices
    if prob_up >= 70:
        trend = "Muy Probablemente Alcista"
    elif prob_up >= 55:
        trend = "Probablemente Alcista"
    elif prob_up >= 45:
        trend = "Lateral con Sesgo Alcista"
    elif prob_up >= 30:
        trend = "Probablemente Bajista"
    else:
        trend = "Muy Probablemente Bajista"

    return round(prob_up, 2), trend


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

    # Calcular indicadores técnicos
    df = calculate_technical_indicators(df)

    # Verificar que hay suficientes datos
    if len(df) < 120:  # Aproximadamente 6 meses de datos (20 días * 6)
        raise ValueError(
            f"Insuficientes datos en {csv_file}. Se requieren al menos 120 días de datos."
        )

    # Eliminar filas con valores NaN
    df = df.dropna()

    if len(df) == 0:
        raise ValueError(f"No hay datos válidos después de procesar {csv_file}")

    # Calcular tendencias para diferentes períodos futuros
    prob_1d, trend_1d = calculate_trend(df, 1)  # Próximo día
    prob_1w, trend_1w = calculate_trend(df, 5)  # Próxima semana
    prob_3m, trend_3m = calculate_trend(df, 60)  # Próximos 3 meses
    prob_6m, trend_6m = calculate_trend(df, 120)  # Próximos 6 meses

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
