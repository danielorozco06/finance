import warnings
from pathlib import Path
from typing import Optional

import pandas as pd

warnings.filterwarnings("ignore")


def format_date(date) -> str:
    """Formatea una fecha a string en formato YYYY-MM-DD."""
    if pd.isna(date):
        return "N/A"
    if isinstance(date, str):
        try:
            return pd.to_datetime(date).strftime("%Y-%m-%d")
        except:
            return date
    if isinstance(date, pd.Timestamp):
        return date.strftime("%Y-%m-%d")
    try:
        return pd.to_datetime(date).strftime("%Y-%m-%d")
    except:
        return str(date)


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

    # Calcular soportes y resistencias
    window_size = 20
    # Primer nivel de soporte y resistencia (más cercano)
    df["Support_1"] = df["Low"].rolling(window=window_size).min()
    df["Resistance_1"] = df["High"].rolling(window=window_size).max()

    # Segundo nivel de soporte y resistencia (medio)
    window_size_2 = 50
    df["Support_2"] = df["Low"].rolling(window=window_size_2).min()
    df["Resistance_2"] = df["High"].rolling(window=window_size_2).max()

    # Tercer nivel de soporte y resistencia (más lejano)
    window_size_3 = 100  # Ventana más amplia para el tercer nivel
    df["Support_3"] = df["Low"].rolling(window=window_size_3).min()
    df["Resistance_3"] = df["High"].rolling(window=window_size_3).max()

    # Calcular distancia a soportes y resistencias
    df["Dist_to_Support_1"] = ((df["Close"] - df["Support_1"]) / df["Close"]) * 100
    df["Dist_to_Resistance_1"] = (
        (df["Resistance_1"] - df["Close"]) / df["Close"]
    ) * 100
    df["Dist_to_Support_2"] = ((df["Close"] - df["Support_2"]) / df["Close"]) * 100
    df["Dist_to_Resistance_2"] = (
        (df["Resistance_2"] - df["Close"]) / df["Close"]
    ) * 100
    df["Dist_to_Support_3"] = ((df["Close"] - df["Support_3"]) / df["Close"]) * 100
    df["Dist_to_Resistance_3"] = (
        (df["Resistance_3"] - df["Close"]) / df["Close"]
    ) * 100

    # Calcular volumen relativo
    df["Volume_MA"] = df["Volume"].rolling(window=20).mean()
    df["Volume_Ratio"] = df["Volume"] / df["Volume_MA"]

    return df


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
        print("\nFechas faltantes detectadas:")
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
        if pd.isna(date):
            return "N/A"
        if isinstance(date, str):
            try:
                return pd.to_datetime(date).strftime("%Y-%m-%d")
            except:
                return date
        if isinstance(date, pd.Timestamp):
            return date.strftime("%Y-%m-%d")
        try:
            return pd.to_datetime(date).strftime("%Y-%m-%d")
        except:
            return str(date)

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
    dist_max_historico = abs(((maximo_historico - last_price) / last_price) * 100)
    dist_min_historico = abs(((last_price - minimo_historico) / last_price) * 100)

    # Calcular distancias a extremos históricos específicos
    dist_max_close = (
        abs(
            (last_price - extremos_historicos["max_close"][0])
            / extremos_historicos["max_close"][0]
        )
        * 100
    )
    dist_min_close = (
        abs((last_price - extremos_historicos["min_close"][0]) / last_price) * 100
    )

    return {
        "ultimo_precio": round(last_price, 2),
        "registros_analizados": len(df),
        "fecha_inicial": format_date(df["Date"].min()),
        "fecha_final": format_date(df["Date"].max()),
        # Análisis de precio
        "precio_maximo_20d": round(df["Close"].rolling(window=20).max().iloc[-1], 2),
        "precio_minimo_20d": round(df["Close"].rolling(window=20).min().iloc[-1], 2),
        # Señales técnicas
        "dist_soporte_1": round(df["Dist_to_Support_1"].iloc[-1], 2),
        "dist_resistencia_1": round(df["Dist_to_Resistance_1"].iloc[-1], 2),
        "valor_soporte_1": round(df["Support_1"].iloc[-1], 2),
        "valor_resistencia_1": round(df["Resistance_1"].iloc[-1], 2),
        "dist_soporte_2": round(df["Dist_to_Support_2"].iloc[-1], 2),
        "dist_resistencia_2": round(df["Dist_to_Resistance_2"].iloc[-1], 2),
        "valor_soporte_2": round(df["Support_2"].iloc[-1], 2),
        "valor_resistencia_2": round(df["Resistance_2"].iloc[-1], 2),
        "dist_soporte_3": round(df["Dist_to_Support_3"].iloc[-1], 2),
        "dist_resistencia_3": round(df["Dist_to_Resistance_3"].iloc[-1], 2),
        "valor_soporte_3": round(df["Support_3"].iloc[-1], 2),
        "valor_resistencia_3": round(df["Resistance_3"].iloc[-1], 2),
        "volumen_relativo": round(df["Volume_Ratio"].iloc[-1], 2),
        # Señales de compra/venta
        "señal_rsi": "Sobrevendida"
        if df["RSI"].iloc[-1] < 30
        else ("Sobrecomprada" if df["RSI"].iloc[-1] > 70 else "Normal"),
        "señal_volumen": "Alto"
        if df["Volume_Ratio"].iloc[-1] > 1.5
        else ("Bajo" if df["Volume_Ratio"].iloc[-1] < 0.5 else "Normal"),
        "señal_precio": "Cerca de Soporte"
        if df["Dist_to_Support_1"].iloc[-1] < 5
        else (
            "Cerca de Resistencia"
            if df["Dist_to_Resistance_1"].iloc[-1] < 5
            else "En Rango Medio"
        ),
        # Indicadores adicionales
        "maximo_1semana": round(last_week["High"].max(), 2),
        "minimo_1semana": round(last_week["Low"].min(), 2),
        "fecha_maximo_1semana": format_date(
            last_week.loc[last_week["High"].idxmax(), "Date"]
        ),
        "fecha_minimo_1semana": format_date(
            last_week.loc[last_week["Low"].idxmin(), "Date"]
        ),
        "maximo_1mes": round(last_month["High"].max(), 2),
        "minimo_1mes": round(last_month["Low"].min(), 2),
        "fecha_maximo_1mes": format_date(
            last_month.loc[last_month["High"].idxmax(), "Date"]
        ),
        "fecha_minimo_1mes": format_date(
            last_month.loc[last_month["Low"].idxmin(), "Date"]
        ),
        "maximo_3meses": round(last_3months["High"].max(), 2),
        "minimo_3meses": round(last_3months["Low"].min(), 2),
        "fecha_maximo_3meses": format_date(
            last_3months.loc[last_3months["High"].idxmax(), "Date"]
        ),
        "fecha_minimo_3meses": format_date(
            last_3months.loc[last_3months["Low"].idxmin(), "Date"]
        ),
        "maximo_6meses": round(last_6months["High"].max(), 2),
        "minimo_6meses": round(last_6months["Low"].min(), 2),
        "fecha_maximo_6meses": format_date(
            last_6months.loc[last_6months["High"].idxmax(), "Date"]
        ),
        "fecha_minimo_6meses": format_date(
            last_6months.loc[last_6months["Low"].idxmin(), "Date"]
        ),
        "maximo_12meses": round(last_12months["High"].max(), 2),
        "minimo_12meses": round(last_12months["Low"].min(), 2),
        "fecha_maximo_12meses": format_date(
            last_12months.loc[last_12months["High"].idxmax(), "Date"]
        ),
        "fecha_minimo_12meses": format_date(
            last_12months.loc[last_12months["Low"].idxmin(), "Date"]
        ),
        "maximo_24meses": round(last_24months["High"].max(), 2),
        "minimo_24meses": round(last_24months["Low"].min(), 2),
        "fecha_maximo_24meses": format_date(
            last_24months.loc[last_24months["High"].idxmax(), "Date"]
        ),
        "fecha_minimo_24meses": format_date(
            last_24months.loc[last_24months["Low"].idxmin(), "Date"]
        ),
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
- Máximo histórico [CLOSE]: ${resultado["maximo_historico_close"]} ({resultado["fecha_maximo_historico_close"]}) [{resultado["dist_max_close"]}% del precio actual]
- Resistencia 3: ${resultado["valor_resistencia_3"]} (distancia: {resultado["dist_resistencia_3"]}%)
- Resistencia 2: ${resultado["valor_resistencia_2"]} (distancia: {resultado["dist_resistencia_2"]}%)
- Resistencia 1: ${resultado["valor_resistencia_1"]} (distancia: {resultado["dist_resistencia_1"]}%)
- >> PRECIO ACTUAL: ${resultado["ultimo_precio"]}
- Soporte 1: ${resultado["valor_soporte_1"]} (distancia: {resultado["dist_soporte_1"]}%)
- Soporte 2: ${resultado["valor_soporte_2"]} (distancia: {resultado["dist_soporte_2"]}%)
- Soporte 3: ${resultado["valor_soporte_3"]} (distancia: {resultado["dist_soporte_3"]}%)
- Mínimo histórico [CLOSE]: ${resultado["minimo_historico_close"]} ({resultado["fecha_minimo_historico_close"]}) [{resultado["dist_min_close"]}% del precio actual]

- RSI: {resultado["señal_rsi"]}
- Volumen: {resultado["señal_volumen"]} (x{resultado["volumen_relativo"]} del promedio)
- Precio: {resultado["señal_precio"]}
"""
    sections.append(header)

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


def filter_report(
    input_dir: str = "tickers_history",
    output_file: str = "input/filter_tickers.md",
    max_distance: float = 5.0,
    exclude_tickers: Optional[list[str]] = None,
    pairs_file: str = "scripts/pares.csv",
    filter_by: list[str] = [
        "max"
    ],  # Lista de criterios: 'max', 'min', 'support', 'resistance'
    max_distances: Optional[
        dict[str, float]
    ] = None,  # Distancias específicas para cada criterio
) -> None:
    """Genera un reporte filtrado de tickers basado en su distancia a diferentes niveles.

    Args:
        input_dir: Directorio donde se encuentran los archivos CSV
        output_file: Archivo de salida para el reporte
        max_distance: Distancia máxima permitida por defecto (porcentaje)
        exclude_tickers: Lista de tickers a excluir del reporte
        pairs_file: Ruta al archivo CSV con los pares de acciones
        filter_by: Lista de criterios de filtrado:
                  'max' para filtrar por distancia al máximo histórico
                  'min' para filtrar por distancia al mínimo histórico
                  'support' para filtrar por distancia al soporte
                  'resistance' para filtrar por distancia a la resistencia
        max_distances: Diccionario con distancias específicas para cada criterio
                      Ejemplo: {'max': 10.0, 'min': 5.0, 'support': 3.0, 'resistance': 3.0}
    """
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    primer_resultado, csv_files = process_ticker_files(input_dir)

    # Validar criterios de filtrado
    valid_criteria = {"max", "min", "support", "resistance"}
    filter_by = [f.lower() for f in filter_by]
    if not all(f in valid_criteria for f in filter_by):
        raise ValueError(f"Criterios de filtrado inválidos. Válidos: {valid_criteria}")

    # Configurar distancias para cada criterio
    distances = max_distances or {f: max_distance for f in filter_by}

    # Obtener tickers a excluir
    pairs_to_exclude = get_pairs_to_exclude(pairs_file)
    exclude_tickers = list(set(t.lower() for t in (exclude_tickers or [])))
    exclude_tickers.extend(t for t in pairs_to_exclude)

    filtered_results = []
    excluded_count = 0

    for csv_file in csv_files:
        try:
            ticker = csv_file.stem.replace("_values", "")
            if ticker in exclude_tickers:
                excluded_count += 1
                continue

            resultado = calculate_stock_probability(str(csv_file))

            # Verificar todos los criterios de filtrado
            meets_criteria = True
            for criterion in filter_by:
                if criterion == "max":
                    distance = float(resultado["dist_max_close"])
                elif criterion == "min":
                    distance = float(resultado["dist_min_close"])
                elif criterion == "support":
                    distance = float(resultado["dist_soporte_1"])
                else:  # resistance
                    distance = float(resultado["dist_resistencia_1"])

                if distance > distances[criterion]:
                    meets_criteria = False
                    break

            if meets_criteria:
                filtered_results.append((ticker, resultado))
        except Exception as e:
            print(f"Error procesando {ticker}: {str(e)}")

    # Ordenar resultados por el primer criterio de filtrado
    sort_key = {
        "max": lambda x: float(x[1]["dist_max_close"]),
        "min": lambda x: float(x[1]["dist_min_close"]),
        "support": lambda x: float(x[1]["dist_soporte_1"]),
        "resistance": lambda x: float(x[1]["dist_resistencia_1"]),
    }
    filtered_results.sort(key=sort_key[filter_by[0]])

    # Generar descripción de criterios
    criteria_desc = []
    for criterion in filter_by:
        dist = distances[criterion]
        if criterion == "max":
            criteria_desc.append(f"máximo histórico ({dist}%)")
        elif criterion == "min":
            criteria_desc.append(f"mínimo histórico ({dist}%)")
        elif criterion == "support":
            criteria_desc.append(f"soporte ({dist}%)")
        else:  # resistance
            criteria_desc.append(f"resistencia ({dist}%)")

    with open(output_file, "w", encoding="utf-8") as f:
        write_report_header(
            f,
            primer_resultado,
            "Análisis de Tendencias de Acciones (Filtrado)",
            f"Mostrando tickers que cumplen con los siguientes criterios:\n"
            f"- Distancia máxima a: {' y '.join(criteria_desc)}\n"
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

    # Lista de tickers a excluir manualmente
    tickers_excluidos: list[str] = []

    # Reporte de acciones cerca de mínimos históricos
    filter_report(
        output_file="input/buy_tickers.md",
        filter_by=["min", "support"],
        max_distances={"min": 80.0, "support": 2.0},
    )

    # Reporte de acciones cerca de máximos históricos
    filter_report(
        output_file="input/sell_tickers.md",
        filter_by=["max", "resistance"],
        max_distances={"max": 40.0, "resistance": 2.0},
    )
