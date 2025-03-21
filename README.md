# Pipeline ETL para Dados de E-Commerce

Este projeto implementa uma pipeline ETL (Extract, Transform, Load) que tem como objetivo extrair dados brutos de um bucket no Google Cloud Platform (GCP), realizar a limpeza e transformação dos dados, e carregá-los em uma tabela do BigQuery para análise aprofundada. A pipeline é projetada para manipular dados transacionais de uma loja online, que opera no Reino Unido e se especializa na venda de presentes únicos para todas as ocasiões. O projeto também inclui um dashboard no Power BI, que pode se conectar diretamente à tabela do BigQuery gerada pela pipeline, permitindo a visualização das métricas e insights dos dados de e-commerce.

O conjunto de dados contém transações realizadas entre 01/12/2010 e 09/12/2011, registrando informações sobre o produto, como código, descrição, quantidade, preço unitário, e os dados do cliente, como ID e país. A seguir, um exemplo de linha do dataset:

| invoiceno | stockcode | description                       | quantity | invoicedate           | unitprice | customerid | country       |
|-----------|-----------|-----------------------------------|----------|-----------------------|-----------|------------|---------------|
| 536365    | 85123A    | WHITE HANGING HEART T-LIGHT HOLDER | 6        | 2010-12-01 08:26:00   | 2.55      | 17850      | United Kingdom |
| 536365    | 71053     | WHITE METAL LANTERN               | 6        | 2010-12-01 08:26:00   | 3.39      | 17850      | United Kingdom |

Este é um conjunto de dados transnacional que contém todas as transações ocorridas entre 01/12/2010 e 09/12/2011 para uma empresa online registrada no Reino Unido. A empresa vende principalmente presentes exclusivos para todas as ocasiões, e muitos de seus clientes são atacadistas.

## Estrutura do Projeto

O projeto está organizado em três pastas principais:

- **E-Commerce Data**: Contém o dataset bruto (data.csv) que deve ser feito o upload para o seu bucket no GCP.
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
gcloud config get-value project
```

- **Bucket no GCS**: Crie um bucket no GCS e faça o upload do arquivo data.csv.

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
BUCKET_NAME = "case-pipeline-etl-ecommerce" # Substitua nome do seu bucket
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
O dashboard no Power BI está configurado para se conectar diretamente à tabela do BigQuery que será gerada pela pipeline. Para utilizá-lo:

1. Baixe o arquivo do dashboard em formato .pbix.
2. Abra o arquivo no Power BI.
3. Conecte-se ao BigQuery usando suas credenciais do GCP.
4. Visualize e explore os dados e métricas de e-commerce conforme a tabela gerada pela pipeline.

## Decisões de Projeto

Durante o desenvolvimento desta pipeline ETL, várias decisões foram tomadas para garantir que o projeto fosse eficiente, escalável e de fácil manutenção. Abaixo estão as principais decisões e suas justificativas:

### 1. **Escolha de Scripts Python para a Pipeline**
   - **Decisão**: Optei por implementar a pipeline utilizando scripts Python em vez de ferramentas de orquestração como Apache Airflow.
   - **Justificativa**: 
     - A pipeline não é complexa o suficiente para justificar o uso de um orquestrador como o Airflow. A simplicidade dos scripts Python permite uma execução direta e fácil de entender.
     - No entanto, a estrutura do projeto foi pensada para ser facilmente adaptável ao Airflow no futuro, caso a necessidade de orquestração e agendamento de tarefas se torne relevante.

### 2. **Organização de Arquivos Processados por Data**
   - **Decisão**: Implementei uma função que salva o dataset limpo em uma pasta nomeada com a data de execução da pipeline.
   - **Justificativa**:
     - Isso permite um histórico de execuções da pipeline, facilitando a auditoria e a recuperação de dados processados em datas específicas.
     - A organização por data também ajuda a evitar sobreposição de arquivos e mantém o bucket do GCS organizado.

### 3. **Criação da Coluna `totalprice`**
   - **Decisão**: Adicionei uma coluna derivada chamada `totalprice`, que calcula o valor total de cada transação (quantidade × preço unitário).
   - **Justificativa**:
     - Essa coluna é essencial para análises financeiras, como cálculo de receita total, média de vendas por transação e outras métricas de negócios.
     - O arredondamento para duas casas decimais garante precisão e consistência nos cálculos.

### 4. **Processos de Limpeza e Transformação**
   - **Decisão**: Implementei uma série de processos de limpeza e transformação, incluindo:
     - Remoção de linhas com valores faltantes ou inválidos.
     - Conversão de tipos de dados para garantir consistência.
     - Remoção de duplicatas e dados inconsistentes (como `quantity <= 0` ou `unitprice <= 0`).
   - **Justificativa**:
     - Esses processos garantem a qualidade dos dados, eliminando inconsistências que poderiam comprometer as análises.
     - A remoção de duplicatas e dados inválidos evita distorções nos resultados finais.

### 5. **Uso do Google Cloud Platform (GCP)**
   - **Decisão**: Utilizei o GCP para armazenamento (Google Cloud Storage) e processamento de dados (BigQuery).
   - **Justificativa**:
     - O GCP oferece uma infraestrutura escalável e confiável para pipelines de dados.
     - A integração entre GCS e BigQuery é simples e eficiente, permitindo carregar grandes volumes de dados rapidamente.

### 6. **Dashboard no Power BI**
   - **Decisão**: Incluí um dashboard no Power BI conectado diretamente à tabela do BigQuery.
   - **Justificativa**:
     - O Power BI é uma ferramenta poderosa para visualização de dados, permitindo a criação de relatórios interativos e dashboards intuitivos.
     - A conexão direta com o BigQuery garante que os dados exibidos estejam sempre atualizados.

### 7. **Facilidade de Replicação e Adaptação**
   - **Decisão**: O projeto foi desenvolvido de forma modular, com scripts separados para extração/transformação e carga.
   - **Justificativa**:
     - Essa modularidade facilita a replicação da pipeline para outros projetos ou a adaptação para uso com ferramentas de orquestração como Airflow.
     - A estrutura do código também permite a inclusão de novas etapas de processamento sem afetar o funcionamento existente.


Essas decisões foram tomadas com o objetivo de garantir que a pipeline seja eficiente, escalável e de fácil manutenção, ao mesmo tempo em que atende às necessidades de análise de dados do negócio.

---

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades. Abra uma issue ou envie um pull request.

