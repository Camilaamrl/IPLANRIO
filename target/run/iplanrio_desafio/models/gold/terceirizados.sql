
  
    
    

    create  table
      "terceirizados"."main"."terceirizados__dbt_tmp"
  
    as (
      

SELECT
    id_terceirizado,
    terceirizado_nome,
    cpf,
    salario_valor,
    orgao_superior_sigla,
    empresa_cnpj,
    CURRENT_TIMESTAMP AS data_carga_datahora,
    mes_particao
FROM "terceirizados"."main"."stg_terceirizados"
    );
  
  