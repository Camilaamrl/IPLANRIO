{{ config(
    materialized='incremental',
    unique_key='id_terceirizado'
) }}

WITH bronze AS (
    SELECT * FROM {{ ref('terceirizados_bronze') }}
)

SELECT
    CAST(id_terc AS STRING) AS id_terceirizado,
    -- Usando a alternativa ao INITCAP que funcionou anteriormente
    UPPER(LEFT(nm_terceirizado, 1)) || LOWER(SUBSTRING(nm_terceirizado, 2)) AS terceirizado_nome,
    UPPER(sg_orgao_sup_tabela_ug) AS orgao_superior_sigla,
    nr_cnpj AS empresa_cnpj,
    nr_cpf AS cpf,
    CAST(vl_mensal_salario AS DECIMAL(18,2)) AS salario_valor,
    CAST(Mes_Carga AS STRING) || '-' || CAST(Ano_Carga AS STRING) AS mes_particao
FROM bronze

{% if is_incremental() %}
  -- Garante a idempotência: não processa IDs que já estão na tabela prata
  WHERE id_terceirizado NOT IN (SELECT id_terceirizado FROM {{ this }})
{% endif %}