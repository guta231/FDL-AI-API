import connection_db

def search_registry(search_field, search_value):
    connection = connection_db.init_database()
    if not connection:
        return None
    
    able_fields = ['VIN_Hash', 'MaintenanceID', 'ID']
    if search_field not in able_fields:
        return None
        
    try:
        with connection.cursor() as cursor:
 
            query = f"SELECT * FROM dealer_flow.dealer_code_ml WHERE {search_field} = %s ORDER BY ServiceDate DESC LIMIT 1"
            cursor.execute(query, (search_value,))
            result = cursor.fetchone()
            return result
    finally:
        connection.close()

def search_candidates_leads(limit: int):
    connection = connection_db.init_database()
    cursor = connection.cursor()
    

    query = """
        SELECT * FROM dealer_flow.dealer_code_ml 
        WHERE propensity_score IS NOT NULL 
        ORDER BY propensity_score DESC 
        LIMIT %s
    """
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    connection.close()
    
    return results

def update_individual_score(id_customer: int, score: float):
    connection = connection_db.init_database()
    cursor = connection.cursor()
    query = "UPDATE dealer_flow.dealer_code_ml SET propensity_score = %s WHERE ID = %s"
    cursor.execute(query, (score, id_customer))
    connection.commit()
    connection.close()