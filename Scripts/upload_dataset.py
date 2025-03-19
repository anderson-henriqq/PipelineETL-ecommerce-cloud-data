import csv
import psycopg2
from datetime import datetime

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
contador = 0
x = 0


# Função para converter a data para o formato TIMESTAMP usando datetime
def convert_to_timestamp(date_str):
    try:
        # Converter a data para o formato TIMESTAMP (ano-mês-dia hora:minuto:segundo)
        return datetime.strptime(date_str, '%m/%d/%Y %H:%M')
    except Exception as e:
        print(f"Erro ao converter data: {date_str}, Erro: {e}")
        return None


# Abrindo o arquivo CSV com a codificação ISO-8859-1
with open(dataset, 'r', encoding='ISO-8859-1') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Pular o cabeçalho
    for row in csv_reader:
        x = x + 1
        print(x)
        if x == 2000:
            break
        
        # Limpeza dos dados
        # Verificar se há valores nulos e substituir por valores padrão, caso necessário
        if not row[0] or not row[1]:  # Se InvoiceNo ou StockCode estiver vazio
            continue  # Pula a linha
        
        # Limpeza de Quantity e UnitPrice
        try:
            quantity = int(row[3])
            unit_price = float(row[5])
        except ValueError:
            continue  # Se houver erro ao converter os valores, ignora a linha
        
        # Convertendo a data
        invoice_date = convert_to_timestamp(row[4])
        if invoice_date is None:
            continue  # Se a data não puder ser convertida, pula a linha
        
        # Verificando e corrigindo CustomerID (se vazio, substituímos por None)
        customer_id = row[6] if row[6] else None  # Se o valor estiver vazio, substitui por None
        
        # Início da transformação de dados: Insere na tabela vendas
        try:
            # Inserir o produto na tabela vendas
            cur.execute("""
                INSERT INTO vendas (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (row[0], row[1], row[2], quantity, invoice_date, unit_price, customer_id, row[7]))
            conn.commit()  # Confirma a inserção na base de dados
        except Exception as e:
            contador = contador + 1
            falhas.append(f"linha {x} | {row} | Erro: {e}")
            conn.rollback()  # Reverte a transação atual, permitindo a continuação com as próximas linhas
    
# Fechar o cursor e a conexão
cur.close()
conn.close()
print(falhas)
print('Falhas:', contador)
print("Dados carregados com sucesso!")