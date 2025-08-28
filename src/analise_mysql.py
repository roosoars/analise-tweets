import mysql.connector
import re
from textblob import TextBlob
import time

def get_sentiment(text):
    # A MESMA FUNÇÃO USADA NO SPARK
    if text is None:
        return 'Neutro'
    text = ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positivo'
    elif analysis.sentiment.polarity < 0:
        return 'Negativo'
    else:
        return 'Neutro'

# INICIO ANALISE DO MYSQL
start_time = time.time()

print("Conectando ao MySQL...")
# CONEXÃO COM O BANCO DE DADOS
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="projeto_bd"
)
cursor = db.cursor()
print("Buscando dados...")
cursor.execute("SELECT text FROM tweets")
all_tweets = cursor.fetchall()

print("Analisando sentimentos em Python...")
sentiment_counts = {'Positivo': 0, 'Negativo': 0, 'Neutro': 0}
for tweet in all_tweets:
    text = tweet[0]
    sentiment = get_sentiment(text)
    sentiment_counts[sentiment] += 1

end_time = time.time()
duration = end_time - start_time

print("--------------------------------------------------")
print("Contagem de sentimentos nos tweets (via MySQL+Python):")
for sentiment, count in sentiment_counts.items():
    print(f"| {sentiment:<9}| {count:<5}|")
print("--------------------------------------------------")
print(f"Tempo de execução do MySQL+Python: {duration:.4f} segundos")
print("Análise concluída com sucesso!")
