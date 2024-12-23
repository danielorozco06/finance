# Tickers

Ejecutar el script getTickerInfo.py para obtener la información de los tickers.

# Aider

Prompt: Modificar el archivo input/news/economia.md o input/news/politica.md para que contenga un resumen de un parrafo corto de la siguiente noticia con fecha:

# Cursor Composer

@folder > input

## Prompt analisis general

Prompt: Análisis de inversión en acciones colombianas - $(date)

Generar los archivos de análisis:

1. ./output/best_stocks.md: Top 8 acciones recomendadas
2. ./output/worst_stocks.md: Top 8 acciones a evitar
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

Prompt: Crear un archivo .md donde detalles muy claramente tu opinion sobre CNEC y cuando me recomendarias invertir en ella con las siguiente secciones: situacion actual, contexto macroeconomico y sectorial, fortalezas, debilidades, catalizadores futuros, recomendacion de inversion (0-6 meses, 6-18 meses y 18+ meses), niveles tecnicos relevantes, estrategia recomendada, riesgos a monitorear y conclusión.

## Prompt portafolio de inversión

Prompt: Crear un archivo portafolio.md con un portafolio detallado de inversión para un capital de COP 16,000,000 teniendo en cuenta los siguientes criterios:

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

4. Estrategia de gestión del portafolio:

   - Rebalanceos recomendados
   - Ajustes por cambios de mercado
   - Manejo de dividendos
   - Rotación de posiciones

5. Escenarios y contingencias:
   - Plan si mercado sube/baja agresivamente
   - Ajustes por eventos corporativos
   - Estrategia de salida general
