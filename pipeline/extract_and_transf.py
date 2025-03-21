import pandas as pd
from google.cloud import storage
from datetime import datetime
from pytz import timezone

fuso = 'America/Sao_Paulo'
formato_data = '%Y-%m-%d'
data_corrente = datetime.now(timezone(fuso)).strftime(formato_data)

# Configurações do GCS
BUCKET_NAME = "case-pipeline-etl-ecommerce"
FILE_NAME = "data.csv"
PROJECT_ID = "swift-approach-454113-b5"  # Substitua pelo ID do seu projeto
DESTINATION_FOLDER = "processed_data/"+data_corrente  # Pasta de destino no bucket

# 1. Função para baixar o arquivo do GCS
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Baixa um arquivo do bucket do GCS."""
    try:
        # Especifica o projeto ao criar o cliente do GCS
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f"Arquivo {source_blob_name} baixado do bucket {bucket_name} para {destination_file_name}.")
    except Exception as e:
        print(f"Erro ao baixar o arquivo do GCS: {e}")
        raise

# 2. Função para enviar o arquivo para o GCS
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Envia um arquivo para o bucket do GCS."""
    try:
        # Especifica o projeto ao criar o cliente do GCS
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(f"Arquivo {source_file_name} enviado para o bucket {bucket_name} como {destination_blob_name}.")
    except Exception as e:
        print(f"Erro ao enviar o arquivo para o GCS: {e}")
        raise

# 3. Baixar o arquivo CSV do GCS para um arquivo temporário local
try:
    temp_file = "temp_data.csv"
    download_blob(BUCKET_NAME, FILE_NAME, temp_file)
except Exception as e:
    print(f"Erro ao baixar o arquivo do GCS: {e}")
    exit(1)

# 4. Carregar o dataset do arquivo temporário
df = pd.read_csv(temp_file)
initial_rows = len(df)  # Total de linhas no arquivo bruto
print(f"Total de linhas no arquivo bruto: {initial_rows}")

# Adicionar uma coluna com o número da linha original
df['originallinenumber'] = df.index + 1  # +1 porque o índice começa em 0

# 5. Remover linhas com informações faltantes ou em branco
df = df.dropna()  # Remove linhas com qualquer valor nulo
rows_after_missing_clean = len(df)
print(f"Linhas removidas (informações faltantes ou em branco): {initial_rows - rows_after_missing_clean}")
print(f"Execução: Linha {df['originallinenumber'].max()} processada.")

# 6. Verificar se 'unitprice' é um valor numérico
# Converter a coluna 'unitprice' para numérico, forçando valores inválidos para NaN
df['unitprice'] = pd.to_numeric(df['unitprice'], errors='coerce')

# Remover linhas onde 'unitprice' é NaN (valores não numéricos)
rows_before_price_clean = len(df)
df = df.dropna(subset=['unitprice'])
rows_after_price_clean = len(df)
print(f"Linhas removidas (unitprice não numérico): {rows_before_price_clean - rows_after_price_clean}")
print(f"Execução: Linha {df['originallinenumber'].max()} processada.")

# 7. Remover dados inconsistentes ou inválidos
# Remover linhas com quantity <= 0
df = df[df['quantity'] > 0]
rows_after_quantity_clean = len(df)
print(f"Linhas removidas (quantity <= 0): {rows_after_missing_clean - rows_after_quantity_clean}")
print(f"Execução: Linha {df['originallinenumber'].max()} processada.")

# Remover linhas com unitprice <= 0
df = df[df['unitprice'] > 0]
rows_after_price_clean = len(df)
print(f"Linhas removidas (unitprice <= 0): {rows_after_quantity_clean - rows_after_price_clean}")
print(f"Execução: Linha {df['originallinenumber'].max()} processada.")

# Remover linhas com customerid faltante
df = df.dropna(subset=['customerid'])
rows_after_customerid_clean = len(df)
print(f"Linhas removidas (customerid faltante): {rows_after_price_clean - rows_after_customerid_clean}")
print(f"Execução: Linha {df['originallinenumber'].max()} processada.")

# 8. Converter tipos de dados
df['invoicedate'] = pd.to_datetime(df['invoicedate'])
df['customerid'] = df['customerid'].astype(int)

# 9. Criar colunas derivadas
df['totalprice'] = df['quantity'] * df['unitprice']
df['totalprice'] = df['totalprice'].round(2)  # Arredondar para 2 casas decimais

# 10. Remover duplicatas
df = df.drop_duplicates()
rows_after_deduplication = len(df)
print(f"Linhas removidas (duplicatas): {rows_after_customerid_clean - rows_after_deduplication}")
print(f"Execução: Linha {df['originallinenumber'].max()} processada.")

# 11. Remover a coluna originallinenumber (não é mais necessária)
df = df.drop(columns=['originallinenumber'])

# 12. Exportar o dataset limpo
cleaned_file = "cleaned_dataset.csv"
df.to_csv(cleaned_file, index=False)

# 13. Enviar o dataset limpo para uma pasta específica no GCS
destination_blob_name = f"{DESTINATION_FOLDER}{cleaned_file}"  # Caminho completo no bucket
try:
    upload_blob(BUCKET_NAME, cleaned_file, destination_blob_name)
except Exception as e:
    print(f"Erro ao enviar o arquivo limpo para o GCS: {e}")
    exit(1)

# 14. Resumo final
final_rows = len(df)
print(f"Total de linhas removidas: {initial_rows - final_rows}")
print(f"Total de linhas no dataset limpo: {final_rows}")
print(f"Dataset limpo exportado para '{cleaned_file}' e enviado para o bucket {BUCKET_NAME} na pasta '{DESTINATION_FOLDER}'.")