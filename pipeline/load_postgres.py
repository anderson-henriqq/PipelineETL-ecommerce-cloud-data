from datetime import datetime
from pytz import timezone
import pandas as pd
import psycopg2
from google.cloud import storage

# Configuração do fuso horário e formato de data
fuso = 'America/Sao_Paulo'
formato_data = '%Y-%m-%d'
data_corrente = datetime.now(timezone(fuso)).strftime(formato_data)

# Configurações do GCS e PostgreSQL
BUCKET_NAME = "case-pipeline-etl-ecommerce"
FILE_NAME = f"processed_data/{data_corrente}cleaned_dataset.csv"
TEMP_FILE = "temp_cleaned_dataset.csv"
DB_HOST = "34.151.246.67"
DB_PORT = "5432"
DB_NAME = "ecommerce"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
TABLE_NAME = "vendas"

# Função para baixar o arquivo do GCS
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Baixa um arquivo do bucket do GCS."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        
        if not blob.exists():
            print(f"Erro: O arquivo {source_blob_name} não existe no bucket {bucket_name}.")
            return False
        
        blob.download_to_filename(destination_file_name)
        print(f"📥 Arquivo {source_blob_name} baixado para {destination_file_name}.")
        return True
    except Exception as e:
        print(f"❌ Erro ao baixar o arquivo do GCS: {e}")
        return False

# Conectar ao PostgreSQL
def connect_to_postgres():
    """Estabelece conexão com o PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Conexão com PostgreSQL estabelecida!")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
        exit(1)

# Criar a tabela se não existir
def create_table_if_not_exists(conn):
    """Cria a tabela no PostgreSQL se não existir."""
    query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        invoiceno VARCHAR(50),      -- Número da fatura
        stockcode VARCHAR(50),      -- Código do produto
        description TEXT,           -- Descrição do produto
        quantity INTEGER,           -- Quantidade vendida
        invoicedate TIMESTAMP,      -- Data da venda
        unitprice NUMERIC,          -- Preço unitário do produto
        customerid VARCHAR(50),     -- ID do cliente
        country VARCHAR(100),       -- País do cliente
        totalprice NUMERIC          -- Preço total da venda
    )
    """
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
    print(f"✅ Tabela {TABLE_NAME} verificada/criada com sucesso.")

# Inserir dados no PostgreSQL
def insert_data(conn, df):
    """Insere os dados do DataFrame no PostgreSQL."""
    query = f"""
    INSERT INTO {TABLE_NAME} (invoiceno, stockcode, description, quantity, invoicedate, unitprice, customerid, country, totalprice)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        with conn.cursor() as cur:
            for idx, row in df.iterrows():
                # Exibe a linha que está sendo processada
                print(f"📊 Processando linha {idx + 1} de {len(df)}")
                
                # Certifica-se de que os valores estão no formato correto
                data_tuple = (
                    row["invoiceno"], row["stockcode"], row["description"], 
                    int(row["quantity"]), pd.to_datetime(row["invoicedate"]), 
                    float(row["unitprice"]), row["customerid"], row["country"], 
                    float(row["totalprice"])
                )
                cur.execute(query, data_tuple)
        conn.commit()
        print("✅ Dados inseridos com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inserir dados no PostgreSQL: {e}")
        conn.rollback()

# Fluxo principal
if download_blob(BUCKET_NAME, FILE_NAME, TEMP_FILE):
    conn = connect_to_postgres()
    create_table_if_not_exists(conn)
    
    # Carregar CSV para DataFrame
    df = pd.read_csv(TEMP_FILE)

    # Verificar se há dados antes de inserir
    if not df.empty:
        insert_data(conn, df)
    else:
        print("⚠️ Nenhum dado encontrado no arquivo CSV.")

    conn.close()
    print("✅ Processo concluído!")
