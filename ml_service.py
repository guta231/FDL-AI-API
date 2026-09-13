import joblib
import pandas as pd


ai_model = joblib.load('ai_model_ford.pkl')


features_necessary = [
    'DaysLastVisit', 'ModelYear', 'ModelName', 
    'MaintenanceNumber', 'ServiceCode', 'DealerCode', 'KM', 'KM/Day'
]

def predict_probability(data_registry):
    """
    Receive a single registry (dict) and returns the probability of return as a float.
    """

    df = pd.DataFrame([data_registry])
    

    for col in features_necessary:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            df[col] = 0 
            
    X = df[features_necessary].fillna(0)
    

    probability = ai_model.predict_proba(X)[0][1]
    
    return round(probability * 100, 2)