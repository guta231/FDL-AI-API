import joblib
import pandas as pd

# Carrega o "cérebro" para a memória RAM assim que a API iniciar
modelo = joblib.load('modelo_manutencao_rfc.pkl')

# As exatas variáveis que usamos no treinamento
features_necessarias = [
    'DaysLastVisit', 'ModelYear', 'ModelName', 
    'MaintenanceNumber', 'ServiceCode', 'DealerCode', 'KM', 'KM/Day'
]

def prever_probabilidade(dados_registro):
    """
    Recebe um dicionário (JSON) com os dados do cliente, 
    passa pelo modelo e retorna a probabilidade (0.00 a 100.00)
    """
    # Converte o único registro em um DataFrame de 1 linha
    df = pd.DataFrame([dados_registro])
    
    # O Escudo Anti-Texto para evitar travamentos na API
    for col in features_necessarias:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            df[col] = 0 # Prevenção caso falte alguma coluna
            
    X = df[features_necessarias].fillna(0)
    
    # .predict_proba retorna [[Prob_Classe_0, Prob_Classe_1]]
    # Queremos a [0][1], que é a chance matemática de RETORNO.
    probabilidade = modelo.predict_proba(X)[0][1]
    
    return round(probabilidade * 100, 2)