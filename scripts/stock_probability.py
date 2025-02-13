import warnings
from pathlib import Path
from typing import Optional

import pandas as pd
import ta  # Agregar este import

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

    # Calcular soportes y resistencias usando Donchian Channels
    # Primer nivel (más cercano)
    donchian_20 = ta.volatility.DonchianChannel(
        high=df["High"], low=df["Low"], close=df["Close"], window=20
    )
    df["Support_1"] = donchian_20.donchian_channel_lband()
    df["Resistance_1"] = donchian_20.donchian_channel_hband()

    # Segundo nivel (medio)
    donchian_50 = ta.volatility.DonchianChannel(
        high=df["High"], low=df["Low"], close=df["Close"], window=50
    )
    df["Support_2"] = donchian_50.donchian_channel_lband()
    df["Resistance_2"] = donchian_50.donchian_channel_hband()

    # Tercer nivel (más lejano)
    donchian_100 = ta.volatility.DonchianChannel(
        high=df["High"], low=df["Low"], close=df["Close"], window=100
    )
    df["Support_3"] = donchian_100.donchian_channel_lband()
    df["Resistance_3"] = donchian_100.donchian_channel_hband()

    # Rellenar valores NaN con el primer valor disponible
    support_resistance_cols = [
        "Support_1",
        "Resistance_1",
        "Support_2",
        "Resistance_2",
        "Support_3",
        "Resistance_3",
    ]
    df[support_resistance_cols] = df[support_resistance_cols].bfill()

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
        df["Date"] = df["Date"].astype(str)
        df["Date"] = pd.to_datetime(df["Date"].str.split().str[0])
    except Exception as e:
        raise ValueError(f"Error en conversión de fechas: {str(e)}")

    # Eliminar duplicados
    duplicates = df["Date"].duplicated()
    if duplicates.any():
        df = df.drop_duplicates(subset=["Date"], keep="last")

    # Ordenar por fecha
    df = df.sort_values("Date")

    return df


def get_historical_extremes(df: pd.DataFrame) -> tuple[float, str, float, str, dict]:
    """Calcula máximos y mínimos históricos para cada tipo de precio."""
    # Calcular extremos para cada tipo de precio
    extremos = {
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
    """Calcula probabilidades y métricas para un ticker."""
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

    # Calcular indicadores técnicos
    df = calculate_technical_indicators(df)

    # Obtener último precio
    last_price = df["Close"].iloc[-1]

    # Calcular máximos y mínimos históricos
    (
        maximo_historico,
        fecha_maximo_historico,
        minimo_historico,
        fecha_minimo_historico,
        extremos_historicos,
    ) = get_historical_extremes(df)

    # Calcular distancias a extremos históricos
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
        # Agregar máximos y mínimos reales del día
        "maximo_dia": round(df["High"].iloc[-1], 2),
        "minimo_dia": round(df["Low"].iloc[-1], 2),
        "maximo_historico": maximo_historico,
        "fecha_maximo_historico": fecha_maximo_historico,
        "minimo_historico": minimo_historico,
        "fecha_minimo_historico": fecha_minimo_historico,
        "maximo_historico_close": extremos_historicos["max_close"][0],
        "fecha_maximo_historico_close": extremos_historicos["max_close"][1],
        "minimo_historico_close": extremos_historicos["min_close"][0],
        "fecha_minimo_historico_close": extremos_historicos["min_close"][1],
        "dist_max_close": round(dist_max_close, 2),
        "dist_min_close": round(dist_min_close, 2),
    }


def format_report_section(ticker: str, resultado: dict) -> str:
    """Formatea una sección del reporte para un ticker específico."""
    # Calcular diferencia entre distancias
    diferencia = float(resultado["dist_resistencia_1"]) - float(
        resultado["dist_soporte_1"]
    )

    header = f"""## {ticker}
- Máximo histórico [CLOSE]: ${resultado["maximo_historico_close"]} ({resultado["fecha_maximo_historico_close"]}) [{resultado["dist_max_close"]}% del precio actual]
- Resistencia 3: ${resultado["valor_resistencia_3"]} (distancia: {resultado["dist_resistencia_3"]}%)
- Resistencia 2: ${resultado["valor_resistencia_2"]} (distancia: {resultado["dist_resistencia_2"]}%)
- Resistencia 1: ${resultado["valor_resistencia_1"]} (distancia: {resultado["dist_resistencia_1"]}%)
- > PRECIO ACTUAL: ${resultado["ultimo_precio"]}
- Soporte 1: ${resultado["valor_soporte_1"]} (distancia: {resultado["dist_soporte_1"]}%)
- Soporte 2: ${resultado["valor_soporte_2"]} (distancia: {resultado["dist_soporte_2"]}%)
- Soporte 3: ${resultado["valor_soporte_3"]} (distancia: {resultado["dist_soporte_3"]}%)
- Mínimo histórico [CLOSE]: ${resultado["minimo_historico_close"]} ({resultado["fecha_minimo_historico_close"]}) [{resultado["dist_min_close"]}% del precio actual]

- Diferencia R-S: {diferencia:.2f}%
- RSI: {resultado["señal_rsi"]}
- Volumen: {resultado["señal_volumen"]} (x{resultado["volumen_relativo"]} del promedio)
- Precio: {resultado["señal_precio"]}
"""
    return header


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
    """Lee el archivo de pares y determina qué ticker excluir de cada par basado en el precio."""
    if not Path(pairs_file).exists():
        print(f"Archivo de pares no encontrado: {pairs_file}")
        return set()

    try:
        pairs_df = pd.read_csv(pairs_file)
        to_exclude = set()

        for _, row in pairs_df.iterrows():
            ticker1, ticker2 = row["ordinaria"], row["preferencial"]

            try:
                price1 = calculate_stock_probability(
                    f"tickers_history/{ticker1}_values.csv"
                )["ultimo_precio"]
                price2 = calculate_stock_probability(
                    f"tickers_history/{ticker2}_values.csv"
                )["ultimo_precio"]

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
    exclude_tickers: Optional[list[str]] = None,
    pairs_file: str = "scripts/pares.csv",
    max_distances: dict[str, float | str] = None,
) -> None:
    """Genera un reporte filtrado basado en criterios específicos."""
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    primer_resultado, csv_files = process_ticker_files(input_dir)

    # Validar criterios de filtrado
    valid_criteria = {
        "max_inside",
        "max_outside",
        "min_inside",
        "min_outside",
        "support_inside",
        "support_outside",
        "resistance_inside",
        "resistance_outside",
        "r-s",
    }

    if not max_distances:
        raise ValueError("Debe especificar max_distances")

    filter_by = list(max_distances.keys())
    if not all(f in valid_criteria for f in filter_by):
        raise ValueError(f"Criterios de filtrado inválidos. Válidos: {valid_criteria}")

    # Validar valores de r-s
    if "r-s" in max_distances and max_distances["r-s"] not in ["positivo", "negativo"]:
        raise ValueError('El valor para "r-s" debe ser "positivo" o "negativo"')

    # Obtener tickers a excluir
    pairs_to_exclude = get_pairs_to_exclude(pairs_file)
    exclude_tickers = list(set(t.lower() for t in (exclude_tickers or [])))
    exclude_tickers.extend(t for t in pairs_to_exclude)

    filtered_results = []

    for csv_file in csv_files:
        try:
            ticker = csv_file.stem.replace("_values", "")
            if ticker in exclude_tickers:
                continue

            resultado = calculate_stock_probability(str(csv_file))
            meets_criteria = True

            for criterion, value in max_distances.items():
                if criterion == "r-s":
                    dist_resistencia = float(resultado["dist_resistencia_1"])
                    dist_soporte = float(resultado["dist_soporte_1"])
                    diferencia = dist_resistencia - dist_soporte
                    if (value == "positivo" and diferencia <= 0) or (
                        value == "negativo" and diferencia >= 0
                    ):
                        meets_criteria = False
                        break
                elif criterion.startswith("max"):
                    distance = float(resultado["dist_max_close"])
                    if criterion == "max_inside":
                        if distance > value:
                            meets_criteria = False
                            break
                    else:  # max_outside
                        if distance < value:
                            meets_criteria = False
                            break
                elif criterion.startswith("min"):
                    distance = float(resultado["dist_min_close"])
                    if criterion == "min_inside":
                        if distance > value:
                            meets_criteria = False
                            break
                    else:  # min_outside
                        if distance < value:
                            meets_criteria = False
                            break
                elif criterion.startswith("support"):
                    distance = float(resultado["dist_soporte_1"])
                    if criterion == "support_inside":
                        if distance > value:
                            meets_criteria = False
                            break
                    else:  # support_outside
                        if distance < value:
                            meets_criteria = False
                            break
                elif criterion.startswith("resistance"):
                    distance = float(resultado["dist_resistencia_1"])
                    if criterion == "resistance_inside":
                        if distance > value:
                            meets_criteria = False
                            break
                    else:  # resistance_outside
                        if distance < value:
                            meets_criteria = False
                            break

            if meets_criteria:
                filtered_results.append((ticker, resultado))
        except Exception as e:
            print(f"Error procesando {ticker}: {str(e)}")

    # Ordenar resultados siempre por la diferencia R-S
    filtered_results.sort(
        key=lambda x: float(x[1]["dist_resistencia_1"]) - float(x[1]["dist_soporte_1"]),
        reverse=True
        if "r-s" in max_distances and max_distances["r-s"] == "positivo"
        else False,
    )

    # Generar descripción de criterios
    criteria_desc = []
    for criterion, max_distance in max_distances.items():
        base_desc = {
            "max": "máximo histórico",
            "min": "mínimo histórico",
            "support": "soporte",
            "resistance": "resistencia",
            "r-s": "diferencia resistencia-soporte",
        }[criterion.split("_")[0] if "_" in criterion else criterion]

        if criterion == "r-s":
            position = "positiva" if max_distance == "positivo" else "negativa"
            criteria_desc.append(f"{base_desc} debe ser {position}")
        else:
            position = "por debajo" if criterion.endswith("inside") else "por encima"
            criteria_desc.append(f"{base_desc} ({max_distance}%, {position})")

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
    generate_all_report()

    # Reporte de tickers a comprar
    filter_report(
        output_file="input/buy_tickers.md",
        max_distances={
            "max_outside": 0.0,
            "resistance_outside": 0.0,
            "support_inside": 10.0,
            "r-s": "positivo",
        },
    )

    # Reporte de tickers a vender
    filter_report(
        output_file="input/sell_tickers.md",
        max_distances={
            "max_inside": 100.0,
            "resistance_inside": 10.0,
            "support_outside": 0.0,
            "r-s": "negativo",
        },
    )
