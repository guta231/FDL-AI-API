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
            sql = f"SELECT * FROM dealer_code_ML WHERE {campo_busca} = %s ORDER BY ServiceDate DESC LIMIT 1"
            cursor.execute(sql, (valor_busca,))
            resultado = cursor.fetchone()
            return resultado
    finally:
        conexao.close()

def buscar_candidatos_leads(limite=500):
    conexao = connection_db.init_database()
    try:
        with conexao.cursor() as cursor:
            # Puxa clientes recentes que já tem mais de 45 dias desde a última visita (não voltaram recentemente)
            sql = "SELECT * FROM dealer_code_ML WHERE DaysLastVisit > 45 LIMIT %s"
            cursor.execute(sql, (limite,))
            return cursor.fetchall()
    finally:
        conexao.close()