import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores técnicos avanzados para mejorar la predicción."""
    df = df.copy()  # Evitar modificaciones al DataFrame original

    # Rellenar valores faltantes en Close con el último valor disponible
    df["Close"] = df["Close"].fillna(value=df["Close"].ffill())

    # Medias móviles
    df["SMA_5"] = df["Close"].rolling(window=5).mean()
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()

    # Rellenar valores iniciales de medias móviles con el primer valor disponible
    df[["SMA_5", "SMA_20", "SMA_50"]] = df[["SMA_5", "SMA_20", "SMA_50"]].bfill()

    # Volatilidad
    df["Volatility"] = df["Close"].rolling(window=20).std()

    # RSI
    delta = df["Close"].diff()
    delta = pd.to_numeric(delta, errors="coerce")
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    # Evitar división por cero en RSI
    rs = gain / loss.replace(0, float("inf"))
    df["RSI"] = 100 - (100 / (1 + rs))

    # Rellenar RSI con valores neutros
    df["RSI"] = df["RSI"].fillna(value=50)

    # Momentum
    df["Momentum"] = df["Close"] - df["Close"].shift(4)
    df["Momentum"] = df["Momentum"].fillna(value=0)

    # Bollinger Bands
    df["BB_middle"] = df["Close"].rolling(window=20).mean()
    df["BB_upper"] = df["BB_middle"] + 2 * df["Close"].rolling(window=20).std()
    df["BB_lower"] = df["BB_middle"] - 2 * df["Close"].rolling(window=20).std()
    # Rellenar Bollinger Bands con valores conservadores
    df[["BB_middle", "BB_upper", "BB_lower"]] = df[
        ["BB_middle", "BB_upper", "BB_lower"]
    ].fillna(value=df["Close"])

    # Calcular retornos y tendencias
    df["Returns"] = df["Close"].pct_change() * 100
    df["Trend_5d"] = df["Close"].rolling(window=5).mean().pct_change() * 100
    df["Trend_20d"] = df["Close"].rolling(window=20).mean().pct_change() * 100

    # MACD (Moving Average Convergence Divergence)
    exp1 = df["Close"].ewm(span=12, adjust=False).mean()
    exp2 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = exp1 - exp2
    df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["Signal_Line"]

    # Stochastic Oscillator
    low_14 = df["Close"].rolling(window=14).min()
    high_14 = df["Close"].rolling(window=14).max()
    df["%K"] = ((df["Close"] - low_14) / (high_14 - low_14)) * 100
    df["%D"] = df["%K"].rolling(window=3).mean()

    # Average True Range (ATR) para volatilidad
    # Calcular ATR usando solo Close cuando no hay High/Low
    close_diff = abs(df["Close"] - df["Close"].shift(1))
    df["ATR"] = close_diff.rolling(window=14).mean()

    # Fibonacci Retracement Levels
    period_high = df["Close"].rolling(window=20).max()
    period_low = df["Close"].rolling(window=20).min()
    diff = period_high - period_low
    df["Fib_38.2"] = period_high - (diff * 0.382)
    df["Fib_50.0"] = period_high - (diff * 0.500)
    df["Fib_61.8"] = period_high - (diff * 0.618)

    # Calcular soportes y resistencias
    df["Support"] = df["Close"].rolling(window=20).min()
    df["Resistance"] = df["Close"].rolling(window=20).max()

    # Calcular distancia a soportes y resistencias
    df["Dist_to_Support"] = ((df["Close"] - df["Support"]) / df["Close"]) * 100
    df["Dist_to_Resistance"] = ((df["Resistance"] - df["Close"]) / df["Close"]) * 100

    # Calcular volumen relativo
    df["Volume_MA"] = df["Volume"].rolling(window=20).mean()
    df["Volume_Ratio"] = df["Volume"] / df["Volume_MA"]

    return df


def calculate_trend(df: pd.DataFrame, days: int) -> tuple[float, str]:
    """Calcula tendencia usando múltiples factores técnicos."""
    recent_df = df.tail(min(days * 3, len(df)))

    # Inicializar pesos y señales
    signals = {}
    weights = {
        "sma": 0.25,  # Medias móviles
        "rsi": 0.15,  # RSI
        "momentum": 0.15,  # Momentum
        "volatility": 0.15,  # Volatilidad
        "bollinger": 0.15,  # Bandas de Bollinger
        "volume": 0.15,  # Análisis de volumen
    }

    # 1. Tendencia de precio (comparación con medias móviles)
    price = float(recent_df["Close"].iloc[-1])
    sma_5 = float(recent_df["SMA_5"].iloc[-1])
    sma_20 = float(recent_df["SMA_20"].iloc[-1])
    sma_50 = float(recent_df["SMA_50"].iloc[-1])

    # Calcular señal de medias móviles ponderada
    sma_signal = 0
    sma_signal += 0.5 if price > sma_5 else 0  # Corto plazo
    sma_signal += 0.3 if price > sma_20 else 0  # Medio plazo
    sma_signal += 0.2 if price > sma_50 else 0  # Largo plazo
    signals["sma"] = sma_signal

    # 2. RSI
    rsi = float(recent_df["RSI"].iloc[-1])
    # RSI: 0 = sobreventa (señal alcista), 1 = sobrecompra (señal bajista)
    if rsi < 30:
        signals["rsi"] = 1.0  # Fuerte señal alcista
    elif rsi < 45:
        signals["rsi"] = 0.75  # Señal alcista moderada
    elif rsi < 55:
        signals["rsi"] = 0.5  # Neutral
    elif rsi < 70:
        signals["rsi"] = 0.25  # Señal bajista moderada
    else:
        signals["rsi"] = 0  # Fuerte señal bajista

    # 3. Momentum
    momentum = float(recent_df["Momentum"].iloc[-1])
    avg_momentum = float(recent_df["Momentum"].mean())
    signals["momentum"] = 1 if momentum > avg_momentum else (0.5 if momentum > 0 else 0)

    # 4. Volatilidad
    current_volatility = float(recent_df["Volatility"].iloc[-1])
    avg_volatility = float(recent_df["Volatility"].mean())
    vol_ratio = current_volatility / avg_volatility
    signals["volatility"] = 1 if vol_ratio < 0.8 else (0.5 if vol_ratio < 1.2 else 0)

    # 5. Bandas de Bollinger
    bb_position = (price - recent_df["BB_lower"].iloc[-1]) / (
        recent_df["BB_upper"].iloc[-1] - recent_df["BB_lower"].iloc[-1]
    )
    if bb_position < 0.2:
        signals["bollinger"] = 1.0  # Sobreventa
    elif bb_position < 0.4:
        signals["bollinger"] = 0.75
    elif bb_position < 0.6:
        signals["bollinger"] = 0.5
    elif bb_position < 0.8:
        signals["bollinger"] = 0.25
    else:
        signals["bollinger"] = 0  # Sobrecompra

    # 6. Análisis de volumen
    recent_volume = float(recent_df["Volume"].iloc[-1])
    avg_volume = float(recent_df["Volume"].mean())
    vol_price_corr = recent_df["Volume"].corr(recent_df["Close"])
    signals["volume"] = (
        1
        if recent_volume > avg_volume and vol_price_corr > 0
        else (0.5 if recent_volume > avg_volume else 0)
    )

    # Calcular probabilidad ponderada
    prob_up = (
        sum(signal * weights[indicator] for indicator, signal in signals.items()) * 100
    )

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


def validate_csv_structure(df: pd.DataFrame, csv_file: str) -> pd.DataFrame:
    """Valida y limpia la estructura del CSV."""
    # Verificar columnas requeridas
    required_columns = {"Date", "Close", "Volume"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Columnas faltantes en {csv_file}. Se requieren: {required_columns}"
        )

    # Convertir y validar tipos de datos
    try:
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")
    except Exception as e:
        raise ValueError(f"Error en conversión de datos numéricos: {str(e)}")

    # Validar fechas
    try:
        df["Date"] = pd.to_datetime(df["Date"], utc=True)
    except Exception as e:
        raise ValueError(f"Error en conversión de fechas: {str(e)}")

    # Eliminar duplicados
    duplicates = df["Date"].duplicated()
    if duplicates.any():
        print(f"Eliminando {duplicates.sum()} registros duplicados")
        df = df.drop_duplicates(subset=["Date"], keep="last")

    # Ordenar por fecha
    df = df.sort_values("Date")

    # Validar rango de fechas
    date_range = pd.date_range(start=df["Date"].min(), end=df["Date"].max(), freq="B")
    expected_dates = set(date_range)
    actual_dates = set(df["Date"])
    missing_dates = expected_dates - actual_dates

    if missing_dates:
        print(f"\nFechas faltantes detectadas:")
        print(f"- Total días hábiles esperados: {len(expected_dates)}")
        print(f"- Días con datos: {len(actual_dates)}")
        print(f"- Días faltantes: {len(missing_dates)}")

    # Validar valores
    invalid_close = df["Close"].isna().sum()
    invalid_volume = df["Volume"].isna().sum()
    if invalid_close > 0 or invalid_volume > 0:
        print("\nProblemas detectados en los datos:")
        if invalid_close > 0:
            print(f"- {invalid_close} registros sin precio de cierre")
        if invalid_volume > 0:
            print(f"- {invalid_volume} registros sin volumen")

    # Información sobre volumen cero (normal en algunos casos)
    zero_volume = (df["Volume"] == 0).sum()
    if zero_volume > 0:
        print(f"\nInformación: {zero_volume} registros con volumen cero")

    return df


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
        initial_rows = len(df)
        print(f"\nProcesando {csv_file}")
        print(f"Registros iniciales: {initial_rows}")

    except Exception as e:
        raise ValueError(f"Error al leer el archivo {csv_file}: {str(e)}")

    # Validar y limpiar datos
    df = validate_csv_structure(df, csv_file)

    # Analizar continuidad de datos
    date_range = pd.date_range(start=df["Date"].min(), end=df["Date"].max(), freq="B")
    missing_dates = set(date_range) - set(df["Date"])
    if missing_dates:
        print(
            f"Advertencia: {len(missing_dates)} fechas faltantes en el rango de datos"
        )

    print(
        f"Rango de fechas: {df['Date'].min().strftime('%Y-%m-%d')} a {df['Date'].max().strftime('%Y-%m-%d')}"
    )
    print(f"Días hábiles en el rango: {len(date_range)}")
    print(f"Registros disponibles: {len(df)}")

    # Calcular indicadores técnicos
    df = calculate_technical_indicators(df)

    # Verificar que hay suficientes datos
    if len(df) < 120:  # Aproximadamente 6 meses de datos (20 días * 6)
        raise ValueError(
            f"Insuficientes datos en {csv_file}. Se requieren al menos 120 días de datos."
        )

    # Verificar calidad de los datos
    print("\nEstadísticas de datos:")
    print(f"- Total de registros: {len(df)}")
    print(f"- Registros con precio: {df['Close'].notna().sum()}")
    print(f"- Registros con volumen: {df['Volume'].notna().sum()}")

    # Calcular tendencias para diferentes períodos futuros
    prob_1d, trend_1d = calculate_trend(df, 1)  # Próximo día
    prob_1w, trend_1w = calculate_trend(df, 5)  # Próxima semana
    prob_3m, trend_3m = calculate_trend(df, 60)  # Próximos 3 meses
    prob_6m, trend_6m = calculate_trend(df, 120)  # Próximos 6 meses

    # Obtener último precio
    last_price = df["Close"].iloc[-1]
    print(f"Análisis completado usando {len(df)} registros\n")

    # Calcular máximos y mínimos para diferentes períodos
    # 1 semana = 5 días hábiles
    last_week = df.tail(5)
    # 1 mes = ~20 días hábiles
    last_month = df.tail(20)
    # 3 meses = ~60 días hábiles
    last_3months = df.tail(60)
    # 6 meses = ~120 días hábiles
    last_6months = df.tail(120)

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
        "registros_analizados": len(df),
        "fecha_inicial": df["Date"].min().strftime("%Y-%m-%d"),
        "fecha_final": df["Date"].max().strftime("%Y-%m-%d"),
        # Análisis de precio
        "precio_maximo_20d": round(df["Close"].rolling(window=20).max().iloc[-1], 2),
        "precio_minimo_20d": round(df["Close"].rolling(window=20).min().iloc[-1], 2),
        "retorno_1semana": round(last_week["Returns"].mean(), 2),
        "retorno_1mes": round(last_month["Returns"].mean(), 2),
        "retorno_3meses": round(last_3months["Returns"].mean(), 2),
        "retorno_6meses": round(last_6months["Returns"].mean(), 2),
        # Señales técnicas
        "dist_soporte": round(df["Dist_to_Support"].iloc[-1], 2),
        "dist_resistencia": round(df["Dist_to_Resistance"].iloc[-1], 2),
        "volumen_relativo": round(df["Volume_Ratio"].iloc[-1], 2),
        # Señales de compra/venta
        "señal_rsi": "Sobrevendida"
        if df["RSI"].iloc[-1] < 30
        else ("Sobrecomprada" if df["RSI"].iloc[-1] > 70 else "Normal"),
        "señal_volumen": "Alto"
        if df["Volume_Ratio"].iloc[-1] > 1.5
        else ("Bajo" if df["Volume_Ratio"].iloc[-1] < 0.5 else "Normal"),
        "señal_precio": "Cerca de Soporte"
        if df["Dist_to_Support"].iloc[-1] < 5
        else (
            "Cerca de Resistencia"
            if df["Dist_to_Resistance"].iloc[-1] < 5
            else "En Rango Medio"
        ),
        # Indicadores adicionales
        "macd": round(df["MACD"].iloc[-1], 2),
        "macd_signal": round(df["Signal_Line"].iloc[-1], 2),
        "macd_hist": round(df["MACD_Hist"].iloc[-1], 2),
        "stoch_k": round(df["%K"].iloc[-1], 2),
        "stoch_d": round(df["%D"].iloc[-1], 2),
        "atr": round(df["ATR"].iloc[-1], 2),
        "fib_38": round(df["Fib_38.2"].iloc[-1], 2),
        "fib_50": round(df["Fib_50.0"].iloc[-1], 2),
        "fib_61": round(df["Fib_61.8"].iloc[-1], 2),
        # Señales adicionales
        "señal_macd": "Alcista" if df["MACD_Hist"].iloc[-1] > 0 else "Bajista",
        "señal_stoch": "Sobrecompra"
        if df["%K"].iloc[-1] > 80
        else ("Sobreventa" if df["%K"].iloc[-1] < 20 else "Normal"),
        "nivel_fib": "Por encima de 38.2"
        if df["Close"].iloc[-1] > df["Fib_38.2"].iloc[-1]
        else (
            "Entre 38.2 y 50.0"
            if df["Close"].iloc[-1] > df["Fib_50.0"].iloc[-1]
            else (
                "Entre 50.0 y 61.8"
                if df["Close"].iloc[-1] > df["Fib_61.8"].iloc[-1]
                else "Por debajo de 61.8"
            )
        ),
        # Actualizar análisis de máximos y mínimos con fechas y retornos
        "maximo_1semana": round(last_week["Close"].max(), 2),
        "minimo_1semana": round(last_week["Close"].min(), 2),
        "fecha_maximo_1semana": last_week.loc[
            last_week["Close"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_1semana": last_week.loc[
            last_week["Close"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
        "maximo_1mes": round(last_month["Close"].max(), 2),
        "minimo_1mes": round(last_month["Close"].min(), 2),
        "fecha_maximo_1mes": last_month.loc[
            last_month["Close"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_1mes": last_month.loc[
            last_month["Close"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
        "maximo_3meses": round(last_3months["Close"].max(), 2),
        "minimo_3meses": round(last_3months["Close"].min(), 2),
        "fecha_maximo_3meses": last_3months.loc[
            last_3months["Close"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_3meses": last_3months.loc[
            last_3months["Close"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
        "maximo_6meses": round(last_6months["Close"].max(), 2),
        "minimo_6meses": round(last_6months["Close"].min(), 2),
        "fecha_maximo_6meses": last_6months.loc[
            last_6months["Close"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_6meses": last_6months.loc[
            last_6months["Close"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
    }


def generate_tendency_report(
    input_dir: str = "tickers_history", output_file: str = "input/tendency.md"
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
        f.write(f"Generado el: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        for csv_file in csv_files:
            try:
                ticker = csv_file.stem.replace("_values", "")
                resultado = calculate_stock_probability(str(csv_file))

                f.write("\n")
                f.write(f"## {ticker}\n\n")
                f.write(f"- Último precio: ${resultado['ultimo_precio']}\n")
                f.write(
                    f"- Período analizado: {resultado['fecha_inicial']} a {resultado['fecha_final']}\n"
                )
                f.write(
                    f"- Registros analizados: {resultado['registros_analizados']}\n"
                )
                f.write("\n")
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
                    f"- Próximos 6 meses: {resultado['tendencia_prox_6m']} (Prob. subida: {resultado['prob_subida_6m']}%)\n"
                )
                f.write("\n### Análisis Técnico\n")
                f.write("- Rangos históricos:\n")
                f.write(
                    f"  * 1 semana: ${resultado['minimo_1semana']} ({resultado['fecha_minimo_1semana']}) - "
                    f"${resultado['maximo_1semana']} ({resultado['fecha_maximo_1semana']})\n"
                )
                f.write(
                    f"  * 1 mes: ${resultado['minimo_1mes']} ({resultado['fecha_minimo_1mes']}) - "
                    f"${resultado['maximo_1mes']} ({resultado['fecha_maximo_1mes']})\n"
                )
                f.write(
                    f"  * 3 meses: ${resultado['minimo_3meses']} ({resultado['fecha_minimo_3meses']}) - "
                    f"${resultado['maximo_3meses']} ({resultado['fecha_maximo_3meses']})\n"
                )
                f.write(
                    f"  * 6 meses: ${resultado['minimo_6meses']} ({resultado['fecha_minimo_6meses']}) - "
                    f"${resultado['maximo_6meses']} ({resultado['fecha_maximo_6meses']})\n"
                )
                f.write(
                    f"- Retorno Promedio:\n"
                    f"  * 1 semana: {resultado['retorno_1semana']}%\n"
                    f"  * 1 mes: {resultado['retorno_1mes']}%\n"
                    f"  * 3 meses: {resultado['retorno_3meses']}%\n"
                    f"  * 6 meses: {resultado['retorno_6meses']}%\n"
                )
                f.write(f"- Distancia a Soporte: {resultado['dist_soporte']}%\n")
                f.write(
                    f"- Distancia a Resistencia: {resultado['dist_resistencia']}%\n"
                )
                f.write("\n### Análisis Técnico Avanzado\n")
                f.write(
                    f"- MACD: {resultado['señal_macd']} (MACD: {resultado['macd']}, Señal: {resultado['macd_signal']})\n"
                )
                f.write(
                    f"- Estocástico: {resultado['señal_stoch']} (%K: {resultado['stoch_k']}, %D: {resultado['stoch_d']})\n"
                )
                f.write(f"- ATR (Volatilidad): {resultado['atr']}\n")
                f.write("\n### Niveles de Fibonacci\n")
                f.write(f"- Posición actual: {resultado['nivel_fib']}\n")
                f.write(
                    f"- Niveles: 38.2%: ${resultado['fib_38']}, 50%: ${resultado['fib_50']}, 61.8%: ${resultado['fib_61']}\n"
                )
                f.write("\n### Señales de Trading\n")
                f.write(f"- RSI: {resultado['señal_rsi']}\n")
                f.write(
                    f"- Volumen: {resultado['señal_volumen']} (x{resultado['volumen_relativo']} del promedio)\n"
                )
                f.write(f"- Precio: {resultado['señal_precio']}\n")
                f.write("\n")
            except Exception as e:
                f.write(f"## {ticker}\n\n")
                f.write(f"Error al procesar: {str(e)}\n\n")


if __name__ == "__main__":
    generate_tendency_report()
    print("Reporte generado en input/tendency.md")
