
# Pipeline ETL para Dados de E-Commerce

Este projeto consiste em uma pipeline ETL (Extract, Transform, Load) que extrai dados brutos de um bucket no Google Cloud Platform (GCP), realiza a limpeza e transformação dos dados, e os carrega em uma tabela do BigQuery para análise. Além disso, o projeto inclui um dashboard no Power BI conectado à tabela do BigQuery para visualização dos dados.

## Estrutura do Projeto

O projeto está organizado em três pastas principais:

- **E-Commerce Data**: Contém o dataset bruto (data.csv) e um script para baixar o dataset diretamente para o seu bucket no GCP.
- **Pipeline Scripts**: Contém os scripts Python para execução da pipeline ETL:
  - `extract_and_transf.py`: Extrai o dataset do bucket do GCS, realiza a limpeza e transformação dos dados, e envia o dataset limpo para uma pasta específica no GCS.
  - `load_bigquery.py`: Carrega o dataset limpo no BigQuery, criando o dataset e a tabela se necessário.
  - `run_pipeline.sh`: Script shell para automatizar a execução da pipeline.
- **Power BI Dashboard**: Contém o arquivo do dashboard criado no Power BI, que pode ser conectado diretamente à tabela do BigQuery.

## Pré-requisitos

Para executar este projeto, você precisará:

- **Conta no Google Cloud Platform (GCP)**: Crie um projeto no GCP e habilite os serviços Google Cloud Storage (GCS) e BigQuery.
- **SDK do GCP**: Instale e configure o SDK do GCP em sua máquina.
- **Autenticação**: Autentique-se no GCP usando o SDK e defina o projeto padrão.

```bash
gcloud auth login
gcloud config set project [SEU_PROJETO_ID]
```

- **Bucket no GCS**: Crie um bucket no GCS e faça o upload do arquivo data.csv manualmente ou execute o script fornecido para fazer o upload automático.

## Como Executar a Pipeline

### Configuração do Ambiente:

1. Certifique-se de que o SDK do GCP está instalado e configurado.
2. Substitua as variáveis de configuração nos scripts Python (`extract_and_transf.py` e `load_bigquery.py`) com os dados do seu projeto GCP.

### Executando a Pipeline:

Execute o script `run_pipeline.sh` para rodar a pipeline automaticamente.

```bash
./run_pipeline.sh
```

Este script executará os seguintes passos:

- Extração e transformação dos dados (`extract_and_transf.py`).
- Carregamento dos dados no BigQuery (`load_bigquery.py`).

## Detalhes dos Scripts

### `extract_and_transf.py`

Este script realiza a extração do dataset bruto do GCS, faz a limpeza e transformação dos dados, e envia o dataset limpo de volta para o GCS.

```python
import pandas as pd
from google.cloud import storage
from datetime import datetime
from pytz import timezone

# Configurações do GCS
BUCKET_NAME = "case-pipeline-etl-ecommerce"
FILE_NAME = "data.csv"
PROJECT_ID = "swift-approach-454113-b5"  # Substitua pelo ID do seu projeto
DESTINATION_FOLDER = "processed_data/"  # Pasta de destino no bucket

# Funções para download e upload de arquivos no GCS
def download_blob(bucket_name, source_blob_name, destination_file_name):
    # Código para baixar o arquivo do GCS
    pass

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    # Código para enviar o arquivo para o GCS
    pass

# Processo de limpeza e transformação dos dados
# ...
```

### `load_bigquery.py`

Este script carrega o dataset limpo no BigQuery, criando o dataset e a tabela se necessário.

```python
from google.cloud import bigquery
from google.cloud import storage

# Configurações do BigQuery
PROJECT_ID = "swift-approach-454113-b5"  # Substitua pelo ID do seu projeto
DATASET_ID = "ecommerce_dataset"
TABLE_ID = "ecommerce_table"

# Funções para criar dataset e tabela no BigQuery
def create_bigquery_dataset(project_id, dataset_id):
    # Código para criar o dataset no BigQuery
    pass

def create_bigquery_table(project_id, dataset_id, table_id, file_path):
    # Código para criar a tabela no BigQuery
    pass

# Processo de carregamento dos dados no BigQuery
# ...
```

## Dashboard no Power BI
![dashboard](https://github.com/user-attachments/assets/7f149dbb-ea1b-485a-aabe-6fe0242118d0)
O dashboard no Power BI está conectado diretamente à tabela do BigQuery. Para utilizá-lo:

1. Abra o arquivo .pbix no Power BI.
2. Conecte-se ao BigQuery utilizando suas credenciais do GCP.
3. Explore os dados e visualize as métricas de e-commerce.

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades. Abra uma issue ou envie um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

Nota: Certifique-se de substituir as variáveis de configuração nos scripts pelos dados do seu projeto GCP antes de executar a pipeline.
