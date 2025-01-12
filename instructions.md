# Dividendos

Actualizar manualmente el archivo input/dividendos.md con los dividendos de los tickers.

# Aider
CONTEXTO: input/news.md

PROMPT: Modificar el archivo input/news.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha en orden cronologico:

# Tickers

- Ejecutar el script getTickerInfo.py para obtener la información y el historial de los tickers.
- Ejecutar el script stock_probability.py para obtener el análisis de los tickers.

# Cursor Composer

## Prompt analisis individual

CONTEXTO: /input/

PROMPT:

Modificar el archivo ./output/analysis.md con las siguientes secciones para cada ticker:
- Precios recientes: último precio
- Recomendación de inversión: 1 día, 1 semana, 3 meses y 6 meses. Usar etiquetas de VENTA FUERTE, VENTA, MANTENER, COMPRA, COMPRA FUERTE.
NOTA: Hoy es 2025-01-12.
Nota: No crear scripts de python.

## Prompt portafolio de inversión

CONTEXTO: /output/, news.md

PROMPT:

Modificar los archivos ./output/portfolios/1semana.md, 3meses.md y 6meses.md con un portafolio de inversión para un capital de COP 5,000,000.
NOTA: Hoy es 2025-01-12.

Tener en cuenta los siguientes criterios:

1. Tener presente de cada ticker la sección "Recomendación" del archivo ./output/analysis/$TICKER.md para la recomendacion de inversion a X tiempo, omitir tickers con etiqueta MANTENER, VENTA, VENTA FUERTE en el periodo indicado.

2. Organizar el documento con la siguiente estructura:

# Portafolio de Inversión

## 1. Composición

[Distribución por Acción y etiqueta de inversión]

## 2. Plan de Ejecución

Nota: prioriozar compras y ventas escalonadas.

### 2.1 Órdenes de Entrada

[Órdenes de entrada con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.]

### 2.2 Órdenes de Salida

[Órdenes de salida con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.]


Prompt:
Mejorar los portafolios considerando los aspectos clave de las noticias y análisis

---

# Analisis contra portafolio actual

CONTEXTO: output/, dividendos.md y news.md

PROMPT:

Teniendo en cuenta el archivo ./output/miPortafolioActual.md con el portafolio actual, modificar el archivo para optimizar el portafolio con las siguientes secciones:
- "Portafolio Actual"
- "Dividendos y Estrategia de Salida"
Nota: Tener en cuenta que cada orden de compra/venta de acciones tiene un costo de $8000.
NOTA: Hoy es 2025-01-12.


