import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

# CARREGA VARIAVEIS DO .ENV
load_dotenv()

print("Conectando ao MySQL...")
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="projeto_bd"
)
cursor = db.cursor()
print("Conectado!")

# LE O NOME DO ARQUIVO .ENV
input_file = os.getenv("INPUT_CSV_FILE")

print(f"Lendo o arquivo {input_file}...")
df = pd.read_csv(input_file)

print("Inserindo dados na tabela 'tweets'. ISSO VAI DEMORAR BASTANTE...")
count = 0
for index, row in df.iterrows():
    if pd.notna(row['text']):
        sql = "INSERT INTO tweets (text) VALUES (%s)"
        val = (row['text'],)
        cursor.execute(sql, val)
        count += 1
db.commit()
print(f"{count} registros inseridos com sucesso.")
