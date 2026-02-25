from fastapi import FastAPI, Query, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
import duckdb
import os
from contextlib import asynccontextmanager

# Garante que o caminho do banco de dados está correto
DB_PATH = os.path.join("data", "terceirizados.duckdb")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o cache em memória (Requisito do desafio)
    FastAPICache.init(InMemoryBackend())
    yield

app = FastAPI(title="API IPLANRIO - Terceirizados", lifespan=lifespan)

@app.get("/terceirizados")
@cache(expire=60)
async def listar_terceirizados(
    page: int = Query(1, ge=1), 
    size: int = Query(10, ge=1, le=100)
):
    offset = (page - 1) * size
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Banco de dados não encontrado. Rode o dbt run.")
    
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        # Consulta os dados básicos para listagem e paginação
        query = f"""
            SELECT id_terceirizado, orgao_superior_sigla, empresa_cnpj, cpf 
            FROM terceirizados 
            LIMIT {size} OFFSET {offset}
        """
        dados = con.execute(query).df().to_dict(orient="records")
        return {"pagina": page, "tamanho": size, "resultados": dados}
    finally:
        con.close()

@app.get("/terceirizados/{id}")
async def detalhe_terceirizado(id: str):
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        # Busca todos os campos da camada ouro para o ID específico
        query = "SELECT * FROM terceirizados WHERE id_terceirizado = ?"
        resultado = con.execute(query, [id]).df().to_dict(orient="records")
        
        if not resultado:
            raise HTTPException(status_code=404, detail="Terceirizado não encontrado")
            
        return resultado[0]
    finally:
        con.close()