#!/bin/bash

# Definir el query como una variable
query="Análisis de inversión en acciones colombianas - $(date)

Generar los archivos de análisis:
1. ./output/best_stocks.md: Top 10 acciones recomendadas

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

# Verificar que los directorios existan
if [ ! -d "tickers_info" ] || [ ! -d "news" ]; then
    echo "Error: Los directorios tickers_info/ y/o news/ no existen"
    exit 1
fi

# Obtener todos los archivos del directorio tickers_info y news
tickers_files=$(find tickers_info/ -type f)
news_files=$(find news/ -type f)

# Verificar que se encontraron archivos
if [ -z "$tickers_files" ] || [ -z "$news_files" ]; then
    echo "Error: No se encontraron archivos en tickers_info/ y/o news/"
    exit 1
fi

# Combinar ambas listas de archivos y convertirlas en argumentos separados por espacios para --read
read_args=$(echo "$tickers_files $news_files" | tr '\n' ' ' | sed 's/ $//')

# Crear directorio output si no existe
mkdir -p output

# Ejecutar el comando aider
echo "Ejecutando análisis..."
aider --file $read_args --message "$query" --yes-always

echo "Análisis completado."
