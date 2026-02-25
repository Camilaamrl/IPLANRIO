import requests, pandas as pd, boto3, os
from prefect import flow, task
from io import BytesIO

# Configurações do S3 (LocalStack)
S3_CONFIG = {
    "endpoint_url": "http://localhost:4566",
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
    "region_name": "us-east-1"
}

@task(log_prints=True)
def processar_mes(mes):
    s3 = boto3.client('s3', **S3_CONFIG)
    bucket = "iplanrio-bucket"
    key = f"raw/terceirizados_{mes}.parquet"
    
    # Idempotência: Verifica se o arquivo já existe no S3
    try:
        s3.head_object(Bucket=bucket, Key=key)
        print(f"Dados de {mes} já existem. Pulando...")
        return
    except:
        print(f"Processando novo mês: {mes}")

    # Simulando captura (No real, você usaria a URL dos Dados Abertos)
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    res = requests.get(url)
    df = pd.read_csv(BytesIO(res.content))
    
    # Criando colunas da planilha real para o dbt não quebrar
    df['id_terc'] = range(1, len(df) + 1)
    df['nm_terceirizado'] = "Colaborador " + df['id_terc'].astype(str)
    df['sg_orgao_sup'] = "IPLAN"
    df['nr_cnpj'] = "31.546.484/0001-00"
    df['nr_cpf'] = "000.000.000-00"
    df['vl_mensal'] = 5000.00
    
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())

@flow(name="Pipeline IPLANRIO")
def pipeline_principal():
    # Previsão de novos dados (Idempotente)
    meses = ["2025-01", "2025-05", "2025-09"] 
    for mes in meses:
        processar_mes(mes)

if __name__ == "__main__":
    pipeline_principal()