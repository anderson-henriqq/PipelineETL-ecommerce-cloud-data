import psycopg2

conn = psycopg2.connect(
    dbname="ecommerce",
    user="postgres",
    password="postgres",
    host="localhost",  # Ou o IP do servidor, se for remoto
    port="5432"  # A porta padrão do PostgreSQL
)

cur = conn.cursor()

cur.execute(""" 
    CREATE TABLE IF NOT EXISTS vendas (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description TEXT,
    Quantity INT,
    InvoiceDate VARCHAR(50),  
    UnitPrice NUMERIC(10, 2),
    CustomerID INT,
    Country VARCHAR(100)
);
""")

conn.commit()  # Não se esqueça de confirmar a transação
cur.close()  # Fechar o cursor
conn.close()  # Fechar a conexão