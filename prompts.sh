#!/bin/bash

run_aider_query() {
    local query="$1"
    # Obtener todos los archivos del directorio tickers_info y news
    local tickers_files=$(find tickers_info/ -type f)
    local news_files=$(find news/ -type f)

    # Combinar ambas listas de archivos y convertirlas en argumentos separados por espacios para --read
    local read_args=$(echo "$tickers_files $news_files" | tr '\n' ' ' | sed 's/ $//')
    echo "Command: aider --file $read_args --message '$query' --yes-always"
    aider --file $read_args --message "$query" --yes-always
    exit 0
}

# Lista de queries
queries=(
    "Análisis de inversión en acciones colombianas - $(date)

    Generar dos archivos de análisis:
    1. ./output/best_stocks.md: Top 5 acciones recomendadas
    2. ./output/worst_stocks.md: 5 acciones menos recomendadas

    Para cada grupo de acciones, analizar y proyectar rendimiento en:
    - Corto plazo: 1 mes
    - Mediano plazo: 1 año  
    - Largo plazo: 4 años

    Criterios de análisis:
    - Información histórica de los tickers en tickers_info/
    - Noticias y eventos relevantes en news/
    - Contexto macroeconómico actual de Colombia
    - Proyecciones políticas y económicas para cada horizonte temporal
    - Riesgos y oportunidades específicos del mercado colombiano

    Para cada recomendación incluir:
    - Justificación detallada del posicionamiento
    - Factores clave que influyen en la proyección
    - Riesgos específicos a considerar
    - Potencial de valorización/desvalorización estimado

    Formato: Respuesta en español, estructurada y con argumentos respaldados por datos y análisis."
    )

# Ejecutar cada query
for query in "${queries[@]}"
do
    run_aider_query "$query"
done