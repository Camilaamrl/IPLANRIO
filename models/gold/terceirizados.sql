{{ config(materialized='table') }}

SELECT
    id_terceirizado,
    terceirizado_nome,
    cpf,
    salario_valor,
    orgao_superior_sigla,
    empresa_cnpj,
    CURRENT_TIMESTAMP AS data_carga_datahora,
    mes_particao
FROM {{ ref('stg_terceirizados') }}