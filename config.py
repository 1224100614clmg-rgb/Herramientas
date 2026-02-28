import mysql.connector
class Config:
    SECRET_KEY = "sistema_utng_2026_seguro"
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "sql1234"
    MYSQL_DB = "sistema_herramientas"

# Función de conexión 
def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )