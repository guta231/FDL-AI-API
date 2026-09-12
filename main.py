import joblib
from fastapi import FastAPI, HTTPException
import repository

app = FastAPI()

# 1. Carrega a IA na memória do Pi UMA ÚNICA VEZ ao ligar a API
print("Carregando IA na memória...")
modelo_ia = joblib.load('modelo_manutencao_rfc.pkl')

@app.get("/consult/ID/{cliente_id}")
def consultar_cliente(cliente_id: int):
    # CORREÇÃO 1: Usando o nome correto da função e passando 'ID' como campo de busca
    cliente = repository.buscar_registro('ID', cliente_id)
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Registro não encontrado no banco de dados.")
        
    # Verifica se o score já existe no banco
    if cliente.get('propensity_score') is not None:
        cliente['Score_Probabilidade'] = cliente['propensity_score']
        return {"status": "sucesso (via banco)", "dados": cliente}
        
    # CORREÇÃO 2: Substitua os nomes abaixo pelas colunas REAIS que você usou no X_train
    # Exemplo: cliente['Mileage'], cliente['VehicleAge'], etc.
    features = [
        cliente['DaysLastVisit'], 
        cliente['ModelYear'], 
        cliente['ModelName'],
        cliente['MaintenanceNumber'],
        cliente['ServiceCode'],
        cliente['DealerCode'],
        cliente['KM'],
        cliente['KM/Day']
    ] 
    
    score_calculado = float(modelo_ia.predict_proba([features])[0][1])
    
    # Salva no banco para a próxima vez
    repository.atualizar_score_individual(cliente_id, score_calculado)
    
    cliente['Score_Probabilidade'] = score_calculado
    return {"status": "sucesso (via IA sob demanda)", "dados": cliente}

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