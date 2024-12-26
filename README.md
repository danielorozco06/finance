# Tickers

Ejecutar el script getTickerInfo.py para obtener la información de los tickers.

# Aider

PROMPT: Modificar el archivo input/news/economia.md o input/news/politica.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha:

# Cursor Composer

## Prompt analisis general

Skill: Normal

CONTEXTO: /input/

PROMPT: Generar los archivos de análisis pensando en un plazo de 6 meses:

1. ./output/stocks/best.md: Top 7 acciones recomendadas
2. ./output/stocks/worst.md: Top 7 acciones a evitar

Criterios de análisis:

- Información de los tickers en tickers_info/
- Información histórica de los tickers en tickers_history/
- Noticias y eventos relevantes en news/

Nota: La información histórica de los tickers es muy importante para el análisis.

Para cada recomendación incluir:

- Justificación detallada del posicionamiento
- Factores clave que influyen en la proyección
- Riesgos específicos a considerar

Formato: Respuesta en español, estructurada y con argumentos respaldados por datos y análisis.

## Prompt analisis individual

Skill: Agent

CONTEXTO: /input/

PROMPT: Crear los archivos ./output/analysis/$TICKER.md donde se detalle tu opinion sobre cada accion y cuando me recomendarias invertir en ella con las siguiente secciones: situacion actual, contexto macroeconomico y sectorial, fortalezas, debilidades, catalizadores futuros, recomendacion de inversion (0-6 meses, 6-18 meses y 18+ meses), niveles tecnicos relevantes, estrategia recomendada, riesgos a monitorear y conclusion.

## Prompt portafolio de inversión

Skill: Normal

CONTEXTO: /output/

PROMPT: Actualizar el archivo ./output/portfolio.md con un portafolio detallado de inversión para un capital de COP 15,000,000. Tener en cuenta los siguientes criterios:

1. Horizonte temporal de 6 meses
2. Máximo 6 posiciones
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

Comisión por operación: COP 8,000

---

PROMPT: Revisar cada uno de los tickers para ver si se debe agregar o quitar del portafolio

PROMPT: Cuando consideras que seria buen momento para invertir en CNEC?
