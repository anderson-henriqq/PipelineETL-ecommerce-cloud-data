import csv
import psycopg2

# Definir o caminho do arquivo CSV
dataset = '/home/andersonhenriq/Git/PipelineETL-ecommerce-cloud-data/E-Commerce Data/data.csv'  

# Conectando ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="ecommerce",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Lista para armazenar falhas (caso queira armazenar as linhas problemáticas)
falhas = []

# Abrindo o arquivo CSV com a codificação ISO-8859-1
with open(dataset, 'r', encoding='ISO-8859-1') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Pular o cabeçalho
    for row in csv_reader:
        try:
            # Tente inserir a linha no banco de dados
            cur.execute("""
                INSERT INTO vendas (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, row)
            conn.commit()  # Confirma a inserção na base de dados
        except Exception as e:
            # Se um erro ocorrer, exiba a linha e o erro, e desfaça a transação
            print(f"Erro ao inserir linha: {row} | Erro: {e}")
            conn.rollback()  # Reverte a transação atual, permitindo a continuação com as próximas linhas

# Fechar o cursor e a conexão
cur.close()
conn.close()

print("Dados carregados com sucesso!")