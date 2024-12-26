# Tickers

Ejecutar el script getTickerInfo.py para obtener la información de los tickers.

# Aider

PROMPT: Modificar el archivo input/news/economia.md o input/news/politica.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha:

# Cursor Composer

## Prompt analisis individual

CONTEXTO: /input/

PROMPT: Crear el archivo ./output/analysis/$TICKER.md donde se detalle tu opinion sobre cada accion y cuando me recomendarias invertir en ella con las siguiente secciones: situacion actual, contexto macroeconomico y sectorial, fortalezas, debilidades, catalizadores futuros, recomendacion de inversion (0-6 meses, 6-18 meses y 18+ meses), niveles tecnicos relevantes, estrategia recomendada, riesgos a monitorear y conclusion.

## Prompt analisis general

CONTEXTO: /output/analysis/

PROMPT: Teniendo en cuenta la informacion de los archivos de analisis individuales, generar los archivos a un horizonte de 0-6 meses, 6-18 meses y 18+ meses:

1. ./output/stocks/best.md: Top 8 acciones recomendadas
2. ./output/stocks/worst.md: Top 8 acciones a evitar

Para cada recomendación incluir:

- Justificación del posicionamiento
- Factores clave que influyen en la proyección
- Riesgos específicos a considerar

## Prompt portafolio de inversión

CONTEXTO: /output/analysis

PROMPT: Actualizar el archivo ./output/portfolio.md con un portafolio detallado de inversión para un capital de COP 15,000,000 con horizonte temporal a 6 meses, que permita maximizar la rentabilidad teniendo en cuenta los siguientes criterios:

1. Máximo 6 posiciones
2. Tener muy presente la sección "Recomendación de Inversión" de cada ticker
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
   - Horizonte temporal de 1 mes

---

PROMPT: Cuando consideras que seria buen momento para invertir en CNEC y en ECOPETROL?
