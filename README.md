# Tickers

Ejecutar el script getTickerInfo.py para obtener la información de los tickers.

# Aider

PROMPT: Modificar el archivo input/news/economia.md o input/news/politica.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha:

# Cursor Composer

## Prompt analisis individual

CONTEXTO: /input/

PROMPT: Actualizar para cada acción el archivo ./output/analysis/$TICKER.md con las siguientes secciones: fortalezas, debilidades, catalizadores futuros, precio de compra/venta actual, recomendacion de inversion (0-6 meses, 6-18 meses y 18+ meses), niveles tecnicos relevantes, estrategia recomendada. Nota: no incluir dividendos.

## Prompt portafolio de inversión

CONTEXTO: /output/

PROMPT: Actualizar el archivo ./output/portfolio.md con un portafolio diversificado de inversión para un capital de COP 12,000,000. Tener en cuenta los siguientes criterios:

1. Tener muy presente la seccion "Recomendación de Inversión" de cada ticker en el archivo ./output/analysis/$TICKER.md para la recomendacion de inversion a 6 meses
2. Distribución porcentual por acción
3. Plan de entrada escalonado:

   - Montos específicos
   - Precios objetivo de entrada
   - Timing recomendado (inmediato/esperar pullback)

4. Para cada posición incluir:

   - Capital a asignar
   - Precio de entrada objetivo
   - Stop loss inicial
   - Objetivos parciales de ganancia

---

PROMPT: Revisar cada uno de los tickers para ver si se debe agregar o quitar del portafolio

Nota: ejecutar este prompt luego de crear el portafolio de inversión, al menos unas 3 veces para que se genere un portafolio optimo.

---

PROMPT: Cuando consideras que seria buen momento para invertir en CNEC?
