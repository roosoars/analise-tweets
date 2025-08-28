import pandas as pd
import math

# --- CONFIGURAÇÃO ---
ARQUIVO_ORIGINAL = 'Tweets.csv'
ARQUIVO_GRANDE = 'Tweets_10Milhao.csv'
LINHAS_DESEJADAS = 10_000_000

print(f"Lendo o arquivo original '{ARQUIVO_ORIGINAL}'...")
try:
    df_original = pd.read_csv(ARQUIVO_ORIGINAL)
except FileNotFoundError:
    print(f"Erro: Arquivo '{ARQUIVO_ORIGINAL}' não encontrado. Verifique se ele está na pasta.")
    exit()

num_linhas_original = len(df_original)
print(f"O arquivo original tem {num_linhas_original} linhas.")

# CALCULA QUANTAS VEZES PRECISA REPETIR PARA CHEGAR NOS 10 MILHÕES
repeticoes = math.ceil(LINHAS_DESEJADAS / num_linhas_original)

print(f"Repetindo os dados {repeticoes} vezes para gerar {LINHAS_DESEJADAS} linhas...")

# CRIA UMA LISTA DE DATAFRAMES E CONCATENA TODOS DE UMA VEZ AI FICA MAIS EFICIENTE
lista_dfs = [df_original] * repeticoes
df_grande = pd.concat(lista_dfs, ignore_index=True)

# CORTA O DATAFRAME PARA TER EXATAMENTE O NÚMERO DE LINHAS DESEJADO
df_final = df_grande.head(LINHAS_DESEJADAS)

print(f"Salvando o novo arquivo '{ARQUIVO_GRANDE}'...")

# SALVA O NOVO CSV SEM A COLUNA DE INDICE DO PANDAS
df_final.to_csv(ARQUIVO_GRANDE, index=False)

print("--------------------------------------------------")
print(f"✅ Arquivo '{ARQUIVO_GRANDE}' com {len(df_final)} linhas criado com sucesso!")
