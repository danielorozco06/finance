# Dividendos

Actualizar manualmente el archivo input/dividendos.md con los dividendos de los tickers.

# Tickers

Ejecutar el script getTickerInfo.py para obtener la información de los tickers.

# Aider

PROMPT: Modificar el archivo input/news.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha:

# Cursor Composer

## Prompt analisis individual

CONTEXTO: /input/

PROMPT: Modificar para cada acción el archivo ./output/analysis/$TICKER_CL.md con las siguientes secciones: catalizadores futuros, precios de compra/venta mas recientes, recomendacion de inversion (0-1 mes, 0-6 meses, 6-12 meses y etiquetas de VENTA FUERTE, VENTA, MANTENER, COMPRA, COMPRA FUERTE), niveles tecnicos relevantes. Nota: hoy es 2025-01-09.

## Prompt portafolio de inversión

CONTEXTO: /output/, /input/news.md, /input/dividendos.md

PROMPT:Modificar los archivos ./output/portfolios/1mes.md, 6meses.md y 12meses.md con un portafolio diversificado de inversión para un capital de COP 6,000,000. Importante: hoy es 2025-01-02.

Tener en cuenta los siguientes criterios:

1. Tener muy presente la seccion "Recomendación de Inversión" de cada ticker en el archivo ./output/analysis/$TICKER.md para la recomendacion de inversion a X meses. Importante: evitar tickers con etiqueta MANTENER en el periodo indicado y priorizar tickers con etiqueta COMPRA FUERTE.

2. Organizar el documento con la siguiente estructura:

# Portafolio de Inversión

## 1. Composición y Justificación

[Distribución por Acción con sus justificaciones]

## 2. Plan de Ejecución

Nota: prioriozar compras y ventas escalonadas.

### 2.1 Órdenes de Entrada

[Órdenes de entrada con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.]

### 2.2 Órdenes de Protección y Salida

[Stop loss por posición y ordenes de salida con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.]

---

PROMPT: Revisar cada uno de los tickers para ver si se debe agregar o quitar del portafolio

Nota: ejecutar este prompt luego de crear el portafolio de inversión, al menos unas 3 veces para que se genere un portafolio optimo.

---

PROMPT: Cuando consideras que seria buen momento para invertir en CNEC?


# Analisis contra portafolio actual

CONTEXTO: output/, dividendos.md y news.md

PROMPT: Teniendo en cuenta el archivo ./output/miPortafolioActual.md con el portafolio actual de la persona, modificar el archivo para optimizar el portafolio en la secciones de "Dividendos" y "Valores Límite y Fechas Recomendadas para Ventas"?

