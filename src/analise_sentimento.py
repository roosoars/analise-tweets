import re
import os
import time
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
from textblob import TextBlob

load_dotenv()

def get_sentiment(text):
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

start_time = time.time()

app_name = os.getenv("SPARK_APP_NAME")
input_file = os.getenv("INPUT_CSV_FILE")

print("Inicializando a sessão do Spark...")
spark = SparkSession.builder.appName(app_name).master("local[*]").getOrCreate()

print(f"Carregando o arquivo '{input_file}'...")
df = spark.read.option("header", "true").csv(input_file)

df_text = df.select("text")

print("Aplicando a função de análise de sentimento...")
sentiment_udf = udf(get_sentiment, StringType())
df_with_sentiment = df_text.withColumn("sentimento", sentiment_udf(col("text")))

print("--------------------------------------------------")
print("Contagem de sentimentos nos tweets:")
sentiment_counts = df_with_sentiment.groupBy("sentimento").count()
sentiment_counts.show()

end_time = time.time()
duration = end_time - start_time

print("--------------------------------------------------")
print(f"Tempo de execução do Spark: {duration:.2f} segundos")
print("Análise concluída com sucesso!")
print("O código pode ser colocado no GitHub, como sugerido nas diretrizes do projeto.")

spark.stop()
