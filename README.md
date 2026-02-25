# Desafio Engenheiro de Dados - IPLANRIO

Este repositório contém a solução para o desafio técnico de Engenharia de Dados da IPLANRIO. O projeto consiste em uma pipeline de dados utilizando a arquitetura medalhão para processar dados de terceirizados, armazená-los em um banco DuckDB e expô-los através de uma API REST.

## 🏗️ Arquitetura da Solução

A solução segue o padrão de arquitetura medalhão para garantir a organização e qualidade dos dados:

* **Camada Bronze**: Ingestão de dados brutos a partir de arquivos CSV (incluindo dados de jan/mai/set) utilizando a função `read_csv_auto` do DuckDB.
* **Camada Silver**: Etapa de limpeza e padronização. Implementamos o mapeamento de colunas (como `id_terc` para `id_terceirizado`) e o tratamento de codificação de caracteres.
* **Camada Gold**: Tabela de negócio final, otimizada para consulta, contendo os dados higienizados e metadados de carga.

## 🔄 Idempotência e Processamento Incremental

* **Idempotência**: O modelo Silver utiliza a estratégia `incremental` com uma `unique_key`, garantindo que execuções repetidas não dupliquem registros.
* **Escalabilidade**: A pipeline está preparada para ler novos arquivos CSV adicionados à raiz do projeto automaticamente.

## 🛠️ Tecnologias Utilizadas

* **dbt & DuckDB**: Para modelagem SQL e armazenamento eficiente.
* **FastAPI**: Para servir os dados via API REST.
* **Prefect**: Orquestração do fluxo de dados.
* **Docker**: Conteinerização do ambiente.

## 🚀 Como Executar

1.  **Ambiente**: `docker-compose up -d`.
2.  **Pipeline**: `dbt run --full-refresh`.
3.  **API**: `uvicorn app.main:app --reload`.