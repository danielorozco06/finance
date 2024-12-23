# Tickers

Ejecutar el script getTickerInfo.py para obtener la información de los tickers.

# Aider

Prompt: Modificar el archivo input/news/economia.md o input/news/politica.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha:

# Cursor Composer

## Prompt analisis general

CONTEXTO: /input/

PROMPT: Análisis de inversión en acciones colombianas - $(date)

Generar los archivos de análisis:

1. ./output/stocks/best.md: Top 8 acciones recomendadas
2. ./output/stocks/worst.md: Top 8 acciones a evitar
   Para cada grupo de acciones, analizar y proyectar rendimiento en:

- 1 semana
- 1 mes
- 1 año
  Criterios de análisis:
- Información de los tickers en tickers_info/
- Información histórica de los tickers en tickers_history/
- Noticias y eventos relevantes en news/
  Nota: La información histórica de los tickers es muy importante para el análisis.
  Para cada recomendación incluir:
- Justificación detallada del posicionamiento
- Factores clave que influyen en la proyección
- Riesgos específicos a considerar
- Potencial de valorización/desvalorización estimado
  Formato: Respuesta en español, estructurada y con argumentos respaldados por datos y análisis.

## Prompt analisis individual

CONTEXTO: /input/

PROMPT: Crear el archivo ./output/analysis/$TICKER.md donde se detalle tu opinion sobre $TICKER y cuando me recomendarias invertir en ella con las siguiente secciones: situacion actual, contexto macroeconomico y sectorial, fortalezas, debilidades, catalizadores futuros, recomendacion de inversion (0-6 meses, 6-18 meses y 18+ meses), niveles tecnicos relevantes, estrategia recomendada, riesgos a monitorear y conclusión.

## Prompt portafolio de inversión

CONTEXTO: /output/

PROMPT: Crear un archivo portfolio.md con un portafolio detallado de inversión para un capital de COP 15,000,000 teniendo en cuenta los siguientes criterios:

1. Distribución porcentual por acción
2. Plan de entrada escalonado:

   - Montos específicos
   - Precios objetivo de entrada
   - Timing recomendado (inmediato/esperar pullback)

3. Para cada posición incluir:

   - Capital a asignar
   - Precio de entrada objetivo
   - Stop loss inicial
   - Objetivos parciales de ganancia
   - Horizonte temporal recomendado

Muy importante: cada compra/venta paga 8000 COP de comisión.
