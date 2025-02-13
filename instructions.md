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

Modificar el archivo ./output/analysis.md con las siguientes secciones para cada ticker, teniendo muy en cuenta el archivo news.md (noticias y contexto político) y filter_tickers.md:

- Precios:
  - Ultimo precio
  - Máximo histórico [CLOSE]: valor, fecha y distancia
  - Mínimo histórico [CLOSE]: valor, fecha y distancia
  - Soportes: valor y distancia
  - Resistencias: valor y distancia
- Recomendación de inversión:
  - Horizonte de 24 meses: ETIQUETA y pequeña justificación
    Nota: Indicar alguna de las etiquetas: VENTA FUERTE, VENTA, MANTENER, COMPRA, COMPRA FUERTE. La etiqueta debe ser sugerida teniendo en cuenta las noticias del archivo news.md, el analisis del archivo filter_tickers.md.
    Nota: no crear scripts.

PROMPT:

Asegurarme que esten solo los tickers del archivo de filter_tickers.md.

## Prompt portafolio de inversión

CONTEXTO: /output/

PROMPT:

Actualizar completamente los archivos: output/24meses.md; con un portafolio DIVERSIFICADO de inversión para un capital de COP 10,000,000. Tener en cuenta los siguientes criterios:

1. Omitir tickers con etiqueta MANTENER, VENTA, VENTA FUERTE en el periodo indicado. Priorizar COMPRA FUERTE y luego COMPRA
2. Tener en cuenta el precio actual, el mínimo histórico, el máximo histórico, para incluir los tickers con mayor potencial de ganancia en cada periodo de tiempo. Sobre todo para los portafolios de largo plazo.
3. Organizar el documento con la siguiente estructura:

# Portafolio de Inversión

## 1. Composición

[Distribución por Acción, precio actual, etiqueta de inversión, Min. Histórico, soportes (valor y distancia), Max. Histórico y resistencias (valor y distancia)]

## 2. Plan de Ejecución

Nota: prioriozar compras y ventas escalonadas. Tener en cuenta los soportes y resistencias para la ejecución de las ordenes.

### 2.1 Órdenes de Entrada

[Órdenes de entrada con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.] Priorizar ordenes limite.

### 2.2 Órdenes de Salida

[Órdenes de salida con la siguiente estructura: Porcentaje de capital, tipo de orden, precio orden y cantidad de acciones.] Priorizar ordenes limite.

---

# Analisis contra portafolio actual

CONTEXTO: el mismo que el prompt de portafolio de inversión.

PROMPT:

Teniendo en cuenta el archivo miPortafolio.md con el portafolio actual, modificar el archivo para optimizar el portafolio con las siguientes secciones:

- "Portafolio Actual"
- "Dividendos y Estrategia de Salida"
  Nota: Tener en cuenta que cada orden de compra/venta de acciones tiene un costo de $8000.
