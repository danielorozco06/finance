#!/bin/bash

run_aider_query() {
    local query="$1"
    # Obtener todos los archivos del directorio tickers_info
    local files=$(find tickers_info/ -type f)

    # Convertir la lista de archivos en argumentos separados por espacios para --read
    local read_args=$(echo "$files" | tr '\n' ' ' | sed 's/ $//')
    echo "Command: aider --file $read_args --message '$query' --yes-always"
    aider --file $read_args --message "$query" --yes-always
}

# Lista de queries
queries=(
    "crear dos archivos ./output/best_stocks.md y ./output/worst_stocks.md indicando cuales son las 5 mejores y 5 peores acciones \
    de la lista de tickers_info para invertir a un plazo de una semana, un mes y un año. Indicar los argumentos que respaldan la respuesta. Usar español"
)

# Ejecutar cada query
for query in "${queries[@]}"
do
    run_aider_query "$query"
done