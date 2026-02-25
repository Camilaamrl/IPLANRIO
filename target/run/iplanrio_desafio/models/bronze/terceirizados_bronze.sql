
  
  create view "terceirizados"."main"."terceirizados_bronze__dbt_tmp" as (
    

-- O asterisco '*' faz o DuckDB ler o dados.csv, terceirizadosmaio.csv, etc., simultaneamente
SELECT * FROM read_csv_auto(
    '*.csv', 
    delim=';', 
    header=True, 
    ignore_errors=True
)
  );
