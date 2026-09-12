import connection_db

def buscar_registro(campo_busca, valor_busca):
    conexao = connection_db.init_database()
    if not conexao:
        return None
    
    # Prevenção básica de SQL Injection limitando os campos permitidos
    campos_permitidos = ['VIN_Hash', 'MaintenanceID', 'ID']
    if campo_busca not in campos_permitidos:
        return None
        
    try:
        with conexao.cursor() as cursor:
            # Busca o último registro do carro/manutenção
            sql = f"SELECT * FROM dealer_code_ml WHERE {campo_busca} = %s ORDER BY ServiceDate DESC LIMIT 1"
            cursor.execute(sql, (valor_busca,))
            resultado = cursor.fetchone()
            return resultado
    finally:
        conexao.close()

def buscar_candidatos_leads(limite: int):
    conexao = connection_db.init_database()
    cursor = conexao.cursor()
    
    # Busca focada apenas na nova coluna em inglês
    query = """
        SELECT * FROM dealer_flow.dealer_code_ml 
        WHERE propensity_score IS NOT NULL 
        ORDER BY propensity_score DESC 
        LIMIT %s
    """
    cursor.execute(query, (limite,))
    resultados = cursor.fetchall()
    conexao.close()
    
    return resultados