import mysql.connector
from mysql.connector import errorcode

# CONFIGURAÇÃO
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'projeto_bd'
}

try:
    print("Tentando conectar ao MySQL via 127.0.0.1...")
    # TENTA ESTABELECER CONEXÃO
    db = mysql.connector.connect(**config)
    
    print(f"✅ Conexão com o banco '{config['database']}' bem-sucedida!")
    
    # FECHA CONEXÃO
    db.close()
    print("Conexão fechada.")

except mysql.connector.Error as err:
    # PEGA POSSÍVEIS ERROS
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("❌ Erro: Algo está errado com seu usuário ou senha.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(f"❌ Erro: O banco de dados '{config['database']}' não existe.")
    else:
        print(f"❌ Ocorreu um erro inesperado: {err}")
