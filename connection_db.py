import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    try:
        
        connection = pymysql.connect(
            host=os.getenv('HOST_DB'),
            user=os.getenv('USER_DB'),
            port=int(os.getenv('PORT_DB', 3306)),
            password=os.getenv('PASSWORD_DB'),
            database=os.getenv('DATABASE_DB'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("Connected to the database successfully!")
        return connection
    except pymysql.err.OperationalError as e:
        print("Error connecting to the database:", e)
