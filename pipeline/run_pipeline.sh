#!/bin/bash

# Executa a extração e transformação
echo "Iniciando extração e transformação..."
python extract_and_transf.py

# Verifica se o processo anterior foi bem-sucedido
if [ $? -eq 0 ]; then
    echo "Extração e transformação concluídas com sucesso!"
    echo "Iniciando carga no BigQuery..."
    python load_bigquery.py
else
    echo "Erro na extração e transformação. Interrompendo pipeline."
    exit 1
fi

# Verifica se a carga no BigQuery foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "Carga no BigQuery concluída com sucesso!"
else
    echo "Erro ao carregar dados no BigQuery."
    exit 1
fi

echo "Pipeline concluída com sucesso!"
