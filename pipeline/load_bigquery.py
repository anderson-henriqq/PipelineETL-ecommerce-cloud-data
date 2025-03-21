from datetime import datetime
from pytz import timezone
import pandas as pd
from google.cloud import storage, bigquery
from google.api_core.exceptions import NotFound

# Configuração do fuso horário e formato de data
fuso = 'America/Sao_Paulo'
formato_data = '%Y-%m-%d'
data_corrente = datetime.now(timezone(fuso)).strftime(formato_data)

# Configurações do GCS e BigQuery
BUCKET_NAME = "case-pipeline-etl-ecommerce"  # Nome do seu bucket
FILE_NAME = f"processed_data/{data_corrente}cleaned_dataset.csv"  # Caminho do arquivo no bucket
PROJECT_ID = "swift-approach-454113-b5"  # ID do seu projeto
DATASET_ID = "ecommerce_dataset"  # Nome do dataset no BigQuery
TABLE_ID = "ecommerce_table"  # Nome da tabela no BigQuery

# 1. Função para baixar o arquivo do GCS
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Baixa um arquivo do bucket do GCS."""
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)

        if not blob.exists():
            print(f"Erro: O arquivo {source_blob_name} não existe no bucket {bucket_name}.")
            return False
        
        blob.download_to_filename(destination_file_name)
        print(f"Arquivo {source_blob_name} baixado do bucket {bucket_name} para {destination_file_name}.")
        return True
    except Exception as e:
        print(f"Erro ao baixar o arquivo do GCS: {e}")
        return False

# 2. Função para criar o dataset no BigQuery (se não existir)
def create_bigquery_dataset(project_id, dataset_id):
    """Cria um dataset no BigQuery se ele não existir."""
    try:
        bigquery_client = bigquery.Client(project=project_id)
        dataset_ref = bigquery_client.dataset(dataset_id)

        try:
            bigquery_client.get_dataset(dataset_ref)
            print(f"Dataset {dataset_id} já existe.")
        except NotFound:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            bigquery_client.create_dataset(dataset)
            print(f"Dataset {dataset_id} criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o dataset no BigQuery: {e}")
        raise

# 3. Função para criar uma tabela no BigQuery
def create_bigquery_table(project_id, dataset_id, table_id, file_path):
    """Cria uma tabela no BigQuery a partir de um arquivo CSV."""
    try:
        bigquery_client = bigquery.Client(project=project_id)
        table_ref = bigquery_client.dataset(dataset_id).table(table_id)

        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        with open(file_path, "rb") as source_file:
            job = bigquery_client.load_table_from_file(source_file, table_ref, job_config=job_config)

        job.result()
        print(f"Tabela {table_id} criada no dataset {dataset_id} do projeto {project_id}.")
    except Exception as e:
        print(f"Erro ao criar a tabela no BigQuery: {e}")
        raise

# 4. Baixar o arquivo CSV do GCS para um arquivo temporário local
temp_file = "temp_cleaned_dataset.csv"
if not download_blob(BUCKET_NAME, FILE_NAME, temp_file):
    print("Processo abortado devido a erro no download do arquivo.")
    exit(1)

# 5. Criar o dataset no BigQuery (se não existir)
try:
    create_bigquery_dataset(PROJECT_ID, DATASET_ID)
except Exception as e:
    print(f"Erro ao criar o dataset no BigQuery: {e}")
    exit(1)

# 6. Criar a tabela no BigQuery
try:
    create_bigquery_table(PROJECT_ID, DATASET_ID, TABLE_ID, temp_file)
except Exception as e:
    print(f"Erro ao criar a tabela no BigQuery: {e}")
    exit(1)

print("✅ Processo concluído! O arquivo CSV foi carregado no BigQuery com sucesso.")
