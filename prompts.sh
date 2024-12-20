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
    "crear un archivo ./output/stocks_term.md con el resultado de cual es la mejor accion para invertir a corto plazo, mediano plazo y largo plazo"
)

# Ejecutar cada query
for query in "${queries[@]}"
do
    run_aider_query "$query"
done