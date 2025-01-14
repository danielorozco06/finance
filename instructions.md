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

Modificar el archivo ./output/analysis.md con las siguientes secciones para cada ticker del archivo tickerCol.txt:
- Precios recientes: último precio
- Soporte y resistencia: valores y distancias.
- Recomendación de inversión: 1 día, 1 semana, 3 meses y 6 meses. Solo indicar las etiquetas de VENTA FUERTE, VENTA, MANTENER, COMPRA, COMPRA FUERTE. Las etiqueta debe ser sugerida teniendo la ponen cuenta las noticias del archivo input/news.md, el analisis del archivo output/analysis.md, las distancias al soporte y resistencia que permita un posible mejor margen de ganancia. Incluir una muy pequeña justificación de la recomendación. Aumentar el peso de la recomendación de inversión en función de la distancia si es corta al soporte y alta a la resistencia.
NOTA: Hoy es 2025-01-13.

## Prompt portafolio de inversión

CONTEXTO: /output/

PROMPT:

Modificar los archivos ./output/1dia.md, 1semana.md, 3meses.md y 6meses.md con un portafolio de inversión para un capital de COP 5,000,000.
NOTA: Hoy es 2025-01-13.

Tener en cuenta los siguientes criterios:

1. Omitir tickers con etiqueta MANTENER, VENTA, VENTA FUERTE en el periodo indicado.

2. Priorizar acciones con mayor potencial de retorno según distancias a soportes/resistencias

3. Organizar el documento con la siguiente estructura:

# Portafolio de Inversión

## 1. Composición

[Distribución por Acción y etiqueta de inversión]

## 2. Plan de Ejecución

Nota: prioriozar compras y ventas escalonadas.

### 2.1 Órdenes de Entrada

[Órdenes de entrada con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.]

### 2.2 Órdenes de Salida

[Órdenes de salida con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.]

---

# Analisis contra portafolio actual

CONTEXTO: el mismo que el prompt de portafolio de inversión.

PROMPT:

Teniendo en cuenta el archivo ./output/miPortafolio.md con el portafolio actual, modificar el archivo para optimizar el portafolio con las siguientes secciones:
- "Portafolio Actual"
- "Dividendos y Estrategia de Salida"
Nota: Tener en cuenta que cada orden de compra/venta de acciones tiene un costo de $8000.
NOTA: Hoy es 2025-01-13.

# Prompt consultas

CONTEXTO: el mismo que el prompt de analisis individual.

PROMPTS:

Cuando me recomiendas invertir en CNEC?
