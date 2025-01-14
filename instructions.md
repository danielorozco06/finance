# Aider
CONTEXTO: input/news.md

PROMPT: Modificar el archivo input/news.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha en orden cronologico:

# Tickers

- Ejecutar el script scripts/getTickerInfo.py para obtener la información y el historial de los tickers.
- Ejecutar el script scripts/stock_probability.py para obtener el análisis de los tickers.

# Cursor Composer

## Prompt analisis individual

CONTEXTO: /input/

PROMPT:

Modificar el archivo ./output/analysis.md con las siguientes secciones para cada ticker, teniendo en cuenta el archivo news.md y filter_tickers.md:
- Precios: 
  - Ultimo precio
  - Máximo histórico [CLOSE]: valor, fecha y distancia
  - Mínimo histórico [CLOSE]: valor, fecha y distancia
  - Soporte: valor y distancia
  - Resistencia: valor y distancia
- Recomendación de inversión: 
  - A 1 semana: ETIQUETA y pequeña justificación
  - A 3 meses: ETIQUETA y pequeña justificación
  - A 6 meses: ETIQUETA y pequeña justificación
  Nota: Indicar alguna de las etiquetas: VENTA FUERTE, VENTA, MANTENER, COMPRA, COMPRA FUERTE. La etiqueta debe ser sugerida teniendo en cuenta las noticias del archivo news.md, el analisis del archivo filter_tickers.md, las distancias al soporte y resistencia que permita un posible mejor margen de ganancia.
NOTA: Tener presente que hoy es 2025-01-14.

## Prompt portafolio de inversión

CONTEXTO: /output/

PROMPT:

Modificar los archivos 1semana.md, 3meses.md y 6meses.md con un portafolio diversificado de inversión para un capital de COP 5,000,000.
NOTA: Hoy es 2025-01-14.

Tener en cuenta los siguientes criterios:

1. Omitir tickers con etiqueta MANTENER, VENTA, VENTA FUERTE en el periodo indicado. Priorizar COMPRA FUERTE y luego COMPRA

2. Organizar el documento con la siguiente estructura:

# Portafolio de Inversión

## 1. Composición

[Distribución por Acción, etiqueta de inversión, valor de resistencia y soporte, distancia a resistencia y soporte]

## 2. Plan de Ejecución

Nota: prioriozar compras y ventas escalonadas.

### 2.1 Órdenes de Entrada

[Órdenes de entrada con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.] Priorizar ordenes limite.

### 2.2 Órdenes de Salida

[Órdenes de salida con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.] Priorizar ordenes limite.

---

# Analisis contra portafolio actual

CONTEXTO: el mismo que el prompt de portafolio de inversión.

PROMPT:

Teniendo en cuenta el archivo ./output/miPortafolio.md con el portafolio actual, modificar el archivo para optimizar el portafolio con las siguientes secciones:
- "Portafolio Actual"
- "Dividendos y Estrategia de Salida"
Nota: Tener en cuenta que cada orden de compra/venta de acciones tiene un costo de $8000.
NOTA: Hoy es 2025-01-14.

# Prompt consultas

CONTEXTO: el mismo que el prompt de analisis individual.

PROMPTS:

Cuando me recomiendas invertir en CNEC?
