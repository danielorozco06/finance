# Tickers

Ejecutar el script getTickerInfo.py para obtener la información de los tickers.

# Aider

PROMPT: Modificar el archivo input/news/economia.md o input/news/politica.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha:

# Cursor Composer

## Prompt analisis individual

Skill: Agent

CONTEXTO: /input/

PROMPT: Crear para cada acción el archivo ./output/analysis/$TICKER.md con las siguiente secciones: fortalezas, debilidades, catalizadores futuros, recomendacion de inversion (0-6 meses, 6-18 meses y 18+ meses), niveles tecnicos relevantes, estrategia recomendada.

## Prompt portafolio de inversión

Skill: Normal

CONTEXTO: /output/

PROMPT: Actualizar el archivo ./output/portfolio.md con un portafolio de inversión para un capital de COP 15,000,000. Tener en cuenta los siguientes criterios:

1. Tener muy presente la seccion "Recomendación de Inversión" de cada ticker en el archivo ./output/analysis/$TICKER.md
2. Horizonte temporal de 6 meses
3. Distribución porcentual por acción
4. Plan de entrada escalonado:

   - Montos específicos
   - Precios objetivo de entrada
   - Timing recomendado (inmediato/esperar pullback)

5. Para cada posición incluir:

   - Capital a asignar
   - Precio de entrada objetivo
   - Stop loss inicial
   - Objetivos parciales de ganancia

---

PROMPT: Revisar cada uno de los tickers para ver si se debe agregar o quitar del portafolio

PROMPT: Cuando consideras que seria buen momento para invertir en CNEC?
