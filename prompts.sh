#!/bin/bash

run_aider_query() {
    local query="$1"
    # Obtener todos los archivos del directorio actual recursivamente
    local files=$(find . -type f -not -path "*/\.*" -not -path "./venv/*" -not -name "*.pyc")
    # Convertir la lista de archivos en argumentos separados por espacios para --read
    local read_args=$(echo "$files" | tr '\n' ' ' | sed 's/ $//')
    aider --read $read_args --message "$query" --yes-always
}

# Lista de queries
queries=(
    "Crear el archivo conclusions/best_1_stocks.md con los 13 tickers de tickers_info que mas porcentaje de ganancia a corto plazo podrían dar. Usar español"
    "Crear el archivo conclusions/best_2_stocks.md con los 13 tickers de tickers_info que menos porcentaje de ganancia a mediano plazo podrían dar. Usar español"
    "Crear el archivo conclusions/best_3_stocks.md con los 13 tickers de tickers_info que mas porcentaje de ganancia a largo plazo podrían dar. Usar español"
)

# Ejecutar cada query
for query in "${queries[@]}"; do
    run_aider_query "$query"
done