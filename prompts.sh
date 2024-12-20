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
}

# Lista de queries
queries=(
    "La fecha actual es $(date). Crear dos archivos ./output/best_stocks.md y ./output/worst_stocks.md indicando cuales son las 5 mejores y 5 peores acciones \
    de la lista de tickers_info/ para invertir desde hoy hasta un plazo de un mes, 1 año y 4 años. Tener MUY presentes las notas de los archivos 
    de la carpeta news/ para la toma de decisiones y los rangos de tiempo de la inversión según el contexto \
    económico y político que se pudiese dar en esos momentos. Muy importante tener presente el contexto actual del pais, que Colombia. \
    Indicar los argumentos que respaldan la respuesta. Usar español")

# Ejecutar cada query
for query in "${queries[@]}"
do
    run_aider_query "$query"
done