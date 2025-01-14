import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores técnicos avanzados para mejorar la predicción."""
    df = df.copy()  # Evitar modificaciones al DataFrame original

    # Rellenar valores faltantes en Close con el último valor disponible
    df["Close"] = df["Close"].fillna(value=df["Close"].ffill())
    df["High"] = df["High"].fillna(value=df["Close"])  # Usar Close como fallback
    df["Low"] = df["Low"].fillna(value=df["Close"])  # Usar Close como fallback

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
    required_columns = {"Date", "Close", "Volume", "High", "Low"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Columnas faltantes en {csv_file}. Se requieren: {required_columns}"
        )

    # Convertir y validar tipos de datos
    try:
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")
        df["High"] = pd.to_numeric(df["High"], errors="coerce")
        df["Low"] = pd.to_numeric(df["Low"], errors="coerce")
    except Exception as e:
        raise ValueError(f"Error en conversión de datos numéricos: {str(e)}")

    # Convertir y validar fechas
    try:
        # Asegurarnos que la columna Date sea string antes de la conversión
        df["Date"] = df["Date"].astype(str)
        # Intentar convertir a datetime ignorando zonas horarias
        df["Date"] = pd.to_datetime(df["Date"].str.split().str[0])
    except Exception as e:
        raise ValueError(f"Error en conversión de fechas: {str(e)}")

    # Eliminar duplicados
    duplicates = df["Date"].duplicated()
    if duplicates.any():
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
    invalid_high = df["High"].isna().sum()
    invalid_low = df["Low"].isna().sum()

    if invalid_close > 0 or invalid_volume > 0 or invalid_high > 0 or invalid_low > 0:
        print("\nProblemas detectados en los datos:")
        if invalid_close > 0:
            print(f"- {invalid_close} registros sin precio de cierre")
        if invalid_volume > 0:
            print(f"- {invalid_volume} registros sin volumen")
        if invalid_high > 0:
            print(f"- {invalid_high} registros sin precio máximo")
        if invalid_low > 0:
            print(f"- {invalid_low} registros sin precio mínimo")

    # Información sobre volumen cero (normal en algunos casos)
    zero_volume = (df["Volume"] == 0).sum()
    if zero_volume > 0:
        print(f"\nInformación: {zero_volume} registros con volumen cero")

    return df


def get_historical_extremes(df: pd.DataFrame) -> tuple[float, str, float, str, dict]:
    """Calcula máximos y mínimos históricos para cada tipo de precio."""

    def format_date(date) -> str:
        """Formatea una fecha a string en formato YYYY-MM-DD."""
        if isinstance(date, pd.Timestamp):
            return date.strftime("%Y-%m-%d")
        return pd.to_datetime(date).strftime("%Y-%m-%d")

    # Calcular extremos para cada tipo de precio
    extremos = {
        "max_open": (
            round(df["Open"].max(), 2),
            format_date(df.loc[df["Open"].idxmax(), "Date"]),
        ),
        "min_open": (
            round(df["Open"].min(), 2),
            format_date(df.loc[df["Open"].idxmin(), "Date"]),
        ),
        "max_close": (
            round(df["Close"].max(), 2),
            format_date(df.loc[df["Close"].idxmax(), "Date"]),
        ),
        "min_close": (
            round(df["Close"].min(), 2),
            format_date(df.loc[df["Close"].idxmin(), "Date"]),
        ),
        "max_high": (
            round(df["High"].max(), 2),
            format_date(df.loc[df["High"].idxmax(), "Date"]),
        ),
        "min_high": (
            round(df["High"].min(), 2),
            format_date(df.loc[df["High"].idxmin(), "Date"]),
        ),
        "max_low": (
            round(df["Low"].max(), 2),
            format_date(df.loc[df["Low"].idxmax(), "Date"]),
        ),
        "min_low": (
            round(df["Low"].min(), 2),
            format_date(df.loc[df["Low"].idxmin(), "Date"]),
        ),
    }

    # Determinar máximo y mínimo absolutos
    max_value = max(extremos["max_high"][0], extremos["max_close"][0])
    min_value = min(extremos["min_low"][0], extremos["min_close"][0])

    max_date = (
        extremos["max_high"][1]
        if extremos["max_high"][0] >= extremos["max_close"][0]
        else extremos["max_close"][1]
    )
    min_date = (
        extremos["min_low"][1]
        if extremos["min_low"][0] <= extremos["min_close"][0]
        else extremos["min_close"][1]
    )

    return max_value, max_date, min_value, min_date, extremos


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

    # Validar y limpiar datos
    df = validate_csv_structure(df, csv_file)

    # Analizar continuidad de datos
    date_range = pd.date_range(start=df["Date"].min(), end=df["Date"].max(), freq="B")
    missing_dates = set(date_range) - set(df["Date"])

    # Calcular indicadores técnicos
    df = calculate_technical_indicators(df)

    # Calcular tendencias para diferentes períodos futuros
    prob_1w, trend_1w = calculate_trend(df, 5)  # Próxima semana
    prob_3m, trend_3m = calculate_trend(df, 60)  # Próximos 3 meses
    prob_6m, trend_6m = calculate_trend(df, 120)  # Próximos 6 meses

    # Obtener último precio
    last_price = df["Close"].iloc[-1]

    # Calcular máximos y mínimos para diferentes períodos
    # 1 semana = 5 días hábiles
    last_week = df.tail(5)
    # 1 mes = ~20 días hábiles
    last_month = df.tail(20)
    # 3 meses = ~60 días hábiles
    last_3months = df.tail(60)
    # 6 meses = ~120 días hábiles
    last_6months = df.tail(120)
    # 12 meses = ~240 días hábiles en un año
    last_12months = df.tail(240)
    # 24 meses = ~480 días hábiles en dos años
    last_24months = df.tail(480)

    # Calcular máximos y mínimos históricos
    (
        maximo_historico,
        fecha_maximo_historico,
        minimo_historico,
        fecha_minimo_historico,
        extremos_historicos,
    ) = get_historical_extremes(df)

    # Calcular distancias a extremos históricos
    dist_max_historico = ((maximo_historico - last_price) / last_price) * 100
    dist_min_historico = ((last_price - minimo_historico) / last_price) * 100

    # Calcular distancias a extremos históricos específicos
    dist_max_close = (
        (last_price - extremos_historicos["max_close"][0])
        / extremos_historicos["max_close"][0]
    ) * 100
    dist_min_close = (
        (last_price - extremos_historicos["min_close"][0]) / last_price
    ) * 100

    return {
        "ultimo_precio": round(last_price, 2),
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
        "maximo_1semana": round(last_week["High"].max(), 2),
        "minimo_1semana": round(last_week["Low"].min(), 2),
        "fecha_maximo_1semana": last_week.loc[
            last_week["High"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_1semana": last_week.loc[
            last_week["Low"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
        "maximo_1mes": round(last_month["High"].max(), 2),
        "minimo_1mes": round(last_month["Low"].min(), 2),
        "fecha_maximo_1mes": last_month.loc[
            last_month["High"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_1mes": last_month.loc[
            last_month["Low"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
        "maximo_3meses": round(last_3months["High"].max(), 2),
        "minimo_3meses": round(last_3months["Low"].min(), 2),
        "fecha_maximo_3meses": last_3months.loc[
            last_3months["High"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_3meses": last_3months.loc[
            last_3months["Low"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
        "maximo_6meses": round(last_6months["High"].max(), 2),
        "minimo_6meses": round(last_6months["Low"].min(), 2),
        "fecha_maximo_6meses": last_6months.loc[
            last_6months["High"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_6meses": last_6months.loc[
            last_6months["Low"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
        "maximo_12meses": round(last_12months["High"].max(), 2),
        "minimo_12meses": round(last_12months["Low"].min(), 2),
        "fecha_maximo_12meses": last_12months.loc[
            last_12months["High"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_12meses": last_12months.loc[
            last_12months["Low"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
        "maximo_24meses": round(last_24months["High"].max(), 2),
        "minimo_24meses": round(last_24months["Low"].min(), 2),
        "fecha_maximo_24meses": last_24months.loc[
            last_24months["High"].idxmax(), "Date"
        ].strftime("%Y-%m-%d"),
        "fecha_minimo_24meses": last_24months.loc[
            last_24months["Low"].idxmin(), "Date"
        ].strftime("%Y-%m-%d"),
        # Agregar valores de soporte y resistencia
        "valor_soporte": round(df["Support"].iloc[-1], 2),
        "valor_resistencia": round(df["Resistance"].iloc[-1], 2),
        "dist_soporte": round(df["Dist_to_Support"].iloc[-1], 2),
        "dist_resistencia": round(df["Dist_to_Resistance"].iloc[-1], 2),
        # Agregar máximos y mínimos reales del día
        "maximo_dia": round(df["High"].iloc[-1], 2),
        "minimo_dia": round(df["Low"].iloc[-1], 2),
        "maximo_historico": maximo_historico,
        "fecha_maximo_historico": fecha_maximo_historico,
        "minimo_historico": minimo_historico,
        "fecha_minimo_historico": fecha_minimo_historico,
        "dias_faltantes": len(missing_dates),
        "dist_max_historico": round(dist_max_historico, 2),
        "dist_min_historico": round(dist_min_historico, 2),
        "maximo_historico_close": extremos_historicos["max_close"][0],
        "fecha_maximo_historico_close": extremos_historicos["max_close"][1],
        "minimo_historico_close": extremos_historicos["min_close"][0],
        "fecha_minimo_historico_close": extremos_historicos["min_close"][1],
        "dist_max_close": round(dist_max_close, 2),
        "dist_min_close": round(dist_min_close, 2),
    }


def format_report_section(ticker: str, resultado: dict) -> str:
    """Formatea una sección del reporte para un ticker específico."""
    sections = []

    # Sección de encabezado
    header = f"""## {ticker}
- Último precio: ${resultado["ultimo_precio"]}
- Máximo histórico [CLOSE]: ${resultado["maximo_historico_close"]} ({resultado["fecha_maximo_historico_close"]}) [{resultado["dist_max_close"]}% del precio actual]
- Mínimo histórico [CLOSE]: ${resultado["minimo_historico_close"]} ({resultado["fecha_minimo_historico_close"]}) [{resultado["dist_min_close"]}% del precio actual]
- Resistencia: ${resultado["valor_resistencia"]} (distancia: {resultado["dist_resistencia"]}%)
- Soporte: ${resultado["valor_soporte"]} (distancia: {resultado["dist_soporte"]}%)
"""
    sections.append(header)

    # Sección de predicción de tendencias
    trends = """### Predicción de Tendencias
- Próxima semana: {tendencia_prox_1s} (Prob. subida: {prob_subida_1s}%)
- Próximos 3 meses: {tendencia_prox_3m} (Prob. subida: {prob_subida_3m}%)
- Próximos 6 meses: {tendencia_prox_6m} (Prob. subida: {prob_subida_6m}%)
""".format(**resultado)
    sections.append(trends)

    # Sección de señales de trading
    technical = f"""### Señales de Trading
- RSI: {resultado["señal_rsi"]}
- Volumen: {resultado["señal_volumen"]} (x{resultado["volumen_relativo"]} del promedio)
- Precio: {resultado["señal_precio"]}
"""
    sections.append(technical)

    return "\n".join(sections)


def write_report_header(
    file, primer_resultado: dict, titulo: str, info_adicional: str = ""
) -> None:
    """Escribe el encabezado común para todos los reportes."""
    file.write(f"# {titulo}\n\n")
    file.write(f"Generado el: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    file.write(
        f"Período analizado: {primer_resultado['fecha_inicial']} a {primer_resultado['fecha_final']}\n"
    )
    if info_adicional:
        file.write(f"\n{info_adicional}\n")


def process_ticker_files(input_dir: str) -> tuple[dict, list[Path]]:
    """Procesa los archivos de tickers y retorna el primer resultado y la lista de archivos."""
    if not Path(input_dir).is_dir():
        raise NotADirectoryError(f"No se encontró el directorio: {input_dir}")

    csv_files = sorted(
        Path(input_dir).glob("*.csv"), key=lambda x: x.stem.replace("_values", "")
    )
    if not csv_files:
        raise ValueError(f"No se encontraron archivos CSV en {input_dir}")

    primer_resultado = calculate_stock_probability(str(csv_files[0]))
    return primer_resultado, csv_files


def generate_all_report(
    input_dir: str = "tickers_history", output_file: str = "scripts/all_tickers.md"
) -> None:
    """Genera un reporte completo de todos los tickers."""
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    primer_resultado, csv_files = process_ticker_files(input_dir)

    with open(output_file, "w", encoding="utf-8") as f:
        write_report_header(f, primer_resultado, "Análisis de Tendencias de Acciones")

        for csv_file in csv_files:
            try:
                ticker = csv_file.stem.replace("_values", "")
                resultado = calculate_stock_probability(str(csv_file))
                f.write("\n" + format_report_section(ticker, resultado))
            except Exception as e:
                f.write(f"\n## {ticker}\n\nError al procesar: {str(e)}\n\n")


def get_pairs_to_exclude(pairs_file: str) -> set[str]:
    """Lee el archivo de pares y determina qué ticker excluir de cada par basado en el precio.

    Args:
        pairs_file: Ruta al archivo CSV con los pares de acciones

    Returns:
        Set con los tickers a excluir
    """
    if not Path(pairs_file).exists():
        print(f"Archivo de pares no encontrado: {pairs_file}")
        return set()

    try:
        # Leer el archivo de pares
        pairs_df = pd.read_csv(pairs_file)
        to_exclude = set()

        # Para cada par, determinar cuál tiene el precio más alto
        for _, row in pairs_df.iterrows():
            ticker1, ticker2 = row["ordinaria"], row["preferencial"]

            # Obtener precios actuales
            try:
                price1 = calculate_stock_probability(
                    f"tickers_history/{ticker1}_values.csv"
                )["ultimo_precio"]
                price2 = calculate_stock_probability(
                    f"tickers_history/{ticker2}_values.csv"
                )["ultimo_precio"]

                # Excluir el de mayor precio
                if float(price1) > float(price2):
                    to_exclude.add(ticker1)
                else:
                    to_exclude.add(ticker2)
            except Exception as e:
                print(f"Error procesando par {ticker1}/{ticker2}: {str(e)}")
                continue

        return to_exclude

    except Exception as e:
        print(f"Error leyendo archivo de pares: {str(e)}")
        return set()


def generate_filtered_report(
    input_dir: str = "tickers_history",
    output_file: str = "input/filter_tickers.md",
    max_distance: float = 5.0,  # Porcentaje de distancia a máximo histórico
    exclude_tickers: list[str] = None,  # Lista de tickers a excluir
    pairs_file: str = "scripts/pares.csv",  # Archivo con pares ordinaria/preferencial
) -> None:
    """Genera un reporte filtrado de tickers que están lejos de su máximo histórico.

    Args:
        input_dir: Directorio donde se encuentran los archivos CSV
        output_file: Archivo de salida para el reporte
        max_distance: Distancia máxima permitida al máximo histórico (porcentaje)
        exclude_tickers: Lista de tickers a excluir del reporte
        pairs_file: Ruta al archivo CSV con los pares de acciones
    """
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    primer_resultado, csv_files = process_ticker_files(input_dir)

    # Obtener tickers a excluir de los pares
    pairs_to_exclude = get_pairs_to_exclude(pairs_file)

    # Combinar con la lista manual de exclusiones
    exclude_tickers = list(set(t.lower() for t in (exclude_tickers or [])))
    exclude_tickers.extend(t for t in pairs_to_exclude)

    filtered_results = []
    excluded_count = 0

    for csv_file in csv_files:
        try:
            ticker = csv_file.stem.replace("_values", "")
            # Saltar si el ticker está en la lista de exclusión
            if ticker in exclude_tickers:
                excluded_count += 1
                continue

            resultado = calculate_stock_probability(str(csv_file))
            if float(resultado["dist_max_close"]) <= -max_distance:
                filtered_results.append((ticker, resultado))
        except Exception as e:
            print(f"Error procesando {ticker}: {str(e)}")

    filtered_results.sort(key=lambda x: float(x[1]["dist_max_close"]))

    with open(output_file, "w", encoding="utf-8") as f:
        write_report_header(
            f,
            primer_resultado,
            "Análisis de Tendencias de Acciones (Filtrado)",
            f"Mostrando tickers que han caído más de {max_distance}% desde su máximo histórico.\n"
            f"Total de tickers encontrados: {len(filtered_results)}\n"
            + (
                f"Lista de exclusión manual: {', '.join(sorted(set(exclude_tickers) - pairs_to_exclude))}\n"
                if set(exclude_tickers) - pairs_to_exclude
                else ""
            )
            + (
                f"Pares excluidos: {', '.join(sorted(pairs_to_exclude))}"
                if pairs_to_exclude
                else ""
            ),
        )

        for ticker, resultado in filtered_results:
            f.write("\n" + format_report_section(ticker, resultado))


if __name__ == "__main__":
    input_dir = "tickers_history"

    generate_all_report(input_dir)
    print("Reporte general generado")

    # Lista de tickers a excluir
    tickers_excluidos: list[str] = []

    generate_filtered_report(
        input_dir,
        max_distance=2.0,
        exclude_tickers=tickers_excluidos,
        pairs_file="scripts/pares.csv",
    )
