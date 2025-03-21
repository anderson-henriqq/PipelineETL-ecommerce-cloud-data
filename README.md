# Pipeline ETL para Dados de E-Commerce

Este projeto consiste em uma pipeline ETL (Extract, Transform, Load) que extrai dados brutos de um bucket no Google Cloud Platform (GCP), realiza a limpeza e transformação dos dados, e os carrega em uma tabela do BigQuery para análise. Além disso, o projeto inclui um dashboard no Power BI conectado à tabela do BigQuery para visualização dos dados.

## Estrutura do Projeto

O projeto está organizado em três pastas principais:

1. **E-Commerce Data**: Contém o dataset bruto (`data.csv`) e um script para baixar o dataset diretamente para o seu bucket no GCP.
2. **Pipeline Scripts**: Contém os scripts Python para execução da pipeline ETL:
   - `extract_and_transf.py`: Extrai o dataset do bucket do GCS, realiza a limpeza e transformação dos dados, e envia o dataset limpo para uma pasta específica no GCS.
   - `load_bigquery.py`: Carrega o dataset limpo no BigQuery, criando o dataset e a tabela se necessário.
   - `run_pipeline.sh`: Script shell para automatizar a execução da pipeline.
3. **Power BI Dashboard**: Contém o arquivo do dashboard criado no Power BI, que pode ser conectado diretamente à tabela do BigQuery.

## Pré-requisitos

Para executar este projeto, você precisará:

1. **Conta no Google Cloud Platform (GCP)**: Crie um projeto no GCP e habilite os serviços Google Cloud Storage (GCS) e BigQuery.
2. **SDK do GCP**: Instale e configure o SDK do GCP em sua máquina.
3. **Autenticação**: Autentique-se no GCP usando o SDK e defina o projeto padrão.

   ```bash
   gcloud auth login
   gcloud config set project [SEU_PROJETO_ID]

4. **Bucket no GCS  **: Crie um bucket no GCS e faça o upload do arquivo data.csv manualmente ou execute o script fornecido para fazer o upload automático.

# Como Executar a Pipeline

## Configuração do Ambiente:

1. Certifique-se de que o SDK do GCP está instalado e configurado.
   
2. Substitua as variáveis de configuração nos scripts Python (`extract_and_transf.py` e `load_bigquery.py`) com os dados do seu projeto GCP.

## Executando a Pipeline:

Execute o script `run_pipeline.sh` para rodar a pipeline automaticamente.

```bash
./run_pipeline.sh

Este script executará os seguintes passos:

    Extração e transformação dos dados (extract_and_transf.py).

    Carregamento dos dados no BigQuery (load_bigquery.py).


Esse formato vai funcionar bem para o seu `README.md`, fornecendo uma explicação clara sobre a execução da pipeline, incluindo a configuração do ambiente e a execução do script. Se precisar de mais ajustes, é só avisar!

