# Tickers

Ejecutar el script getTickerInfo.py para obtener la información de los tickers.

# Aider

PROMPT: Modificar el archivo input/news.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha:

# Cursor Composer

## Prompt analisis individual

CONTEXTO: /input/

PROMPT: Actualizar para cada acción el archivo ./output/analysis/$TICKER.md con las siguientes secciones: catalizadores futuros, precios de compra/venta mas recientes, recomendacion de inversion (0-6 meses, 6-12 meses y 12-18 meses), niveles tecnicos relevantes. Nota: no incluir dividendos.

## Prompt portafolio de inversión

CONTEXTO: /output/

PROMPT: Actualizar el archivo ./output/portfolio.md con un portafolio diversificado de inversión para un capital de COP 6,000,000.
Tener en cuenta los siguientes criterios:

1. Tener muy presente la seccion "Recomendación de Inversión" de cada ticker en el archivo ./output/analysis/$TICKER.md para la recomendacion de inversion a 6 meses. Evitar tickers sin recomendacion de compra en el periodo indicado.

2. Organizar el documento con la siguiente estructura:

# Portafolio de Inversión

## 1. Composición y Justificación

[Distribución por Acción con sus justificaciones]

## 2. Plan de Ejecución

### 2.1 Órdenes de Entrada

[Órdenes límite de entrada]

### 2.2 Órdenes de Protección

[Stop loss por posición]

### 2.3 Órdenes de Salida

[Take profit por posición]

## 3. Gestión del Portafolio

### 3.1 Gestión de Riesgo

[Stop loss global y reglas de gestión]

### 3.2 Consideraciones de Ejecución

[Reglas de ejecución de órdenes]

### 3.3 Seguimiento y Rebalanceo

[Plan de monitoreo y ajustes]

## 4. Resumen y Notas

[Diversificación y consideraciones importantes]

---

PROMPT: Revisar cada uno de los tickers para ver si se debe agregar o quitar del portafolio

Nota: ejecutar este prompt luego de crear el portafolio de inversión, al menos unas 3 veces para que se genere un portafolio optimo.

---

PROMPT: Cuando consideras que seria buen momento para invertir en CNEC?
