from fastapi import FastAPI, HTTPException
import repository
import ml_service

app = FastAPI(
    title="FDL AI API",
    description="API that return the probability of a customer returning to the dealership within 60 days.",
    version="1.0"
)

@app.get("/consult/{campo}/{valor}")
def consulta_individual(campo: str, valor: str):
    """
    Busca um cliente por VIN_Hash, MaintenanceID ou ID e devolve a probabilidade.
    """
    dados = repository.buscar_registro(campo, valor)
    
    if not dados:
        raise HTTPException(status_code=404, detail="Registro não encontrado no banco de dados.")
    
    # Passa o JSON do cliente pela IA
    prob = ml_service.prever_probabilidade(dados)
    
    # Retorna o JSON completo e insere a probabilidade calculada
    return {
        "status": "sucesso",
        "probabilidade_retorno_60_dias_pct": prob,
        "dados_cliente": dados
    }

@app.get("/top-leads")
def gerar_top_leads(qtd: int = 10):
    """
    Vasculha clientes que não voltaram recentemente, calcula a 
    probabilidade de todos e devolve os top N com maior chance.
    """
    # Busca um lote de candidatos do MySQL
    candidatos = repository.buscar_candidatos_leads(limite=500)
    
    leads_avaliados = []
    for cliente in candidatos:
        prob = ml_service.prever_probabilidade(cliente)
        # Adiciona a propensão direto no dicionário do cliente
        cliente['Score_Probabilidade'] = prob
        leads_avaliados.append(cliente)
    
    # Ordena a lista de clientes pela probabilidade (do maior pro menor)
    leads_avaliados.sort(key=lambda x: x['Score_Probabilidade'], reverse=True)
    
    # Devolve apenas o top N desejado
    return {
        "status": "sucesso",
        "total_analysed": len(candidatos),
        "top_leads": leads_avaliados[:qtd]
    }