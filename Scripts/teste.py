import psycopg2

# Conectando ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="ecommerce",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# Criando o cursor para executar comandos SQL
cur = conn.cursor()

def verdados():
    # Consultando todos os valores da coluna InvoiceNo
    cur.execute("SELECT InvoiceNo FROM vendas;")

    # Recuperando todos os resultados da consulta
    invoices = cur.fetchall()

    contador = 0
    # Exibindo os resultados
    for invoice in invoices:
        contador = contador+1

    print(contador)
    # Fechando o cursor e a conexão
    cur.close()
    conn.close()


def apagardados():
    # Apagando todos os dados da tabela 'vendas'
    cur.execute("TRUNCATE TABLE vendas;")

    # Confirmando as transações
    conn.commit()

    # Fechando o cursor e a conexão
    cur.close()
    conn.close()

    print("Todos os dados foram apagados da tabela vendas.")

verdados()
#apagardados()