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
def gerar_top_leads(quantidade: int = 10):
    # A API vai direto no banco e traz os melhores ranqueados
    candidatos = repository.buscar_candidatos_leads(quantidade)
    
    leads_avaliados = []
    for cliente in candidatos:
        # Apenas pega a probabilidade da nova coluna do banco para manter o formato do JSON
        cliente['Score_Probabilidade'] = cliente.get('propensity_score')
        leads_avaliados.append(cliente)
    
    return {
        "status": "sucesso",
        "top_leads": leads_avaliados
    }