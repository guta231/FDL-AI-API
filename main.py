import joblib
from fastapi import FastAPI, HTTPException
import repository

app = FastAPI()


print("Loading the machine learning model into memory...")
ai_model = joblib.load('ai_model_ford.pkl')

@app.get("/consult/ID/{customer_id}")
def consult_customer(customer_id: int):

    customer = repository.search_registry('ID', customer_id)
    
    if not customer:
        raise HTTPException(status_code=404, detail="Registry not found in the database.")
        

    if customer.get('propensity_score') is not None:
        return {"status": "success (via database)", "data": customer}
        

    features = [
        customer['DaysLastVisit'], 
        customer['ModelYear'], 
        customer['ModelName'],
        customer['MaintenanceNumber'],
        customer['ServiceCode'],
        customer['DealerCode'],
        customer['KM'],
        customer['KM/Day']
    ] 
    
    score_calculated = float(ai_model.predict_proba([features])[0][1])
    

    repository.update_individual_score(customer_id, score_calculated)
    
    customer['propensity_score'] = score_calculated
    return {"status": "success (via IA on-demand)", "data": customer}

@app.get("/top-leads")
def gen_top_leads(qtf: int = 10):

    candidates = repository.search_candidates_leads(qtf)
    
    leads_available = []
    for customer in candidates:

        leads_available.append(customer)
    
    return {
        "status": "success",
        "top_leads": leads_available
    }