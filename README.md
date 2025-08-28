# Análise de Sentimentos em Tweets (Spark + MySQL)

Este projeto implementa um **pipeline de Big Data** para análise de sentimentos em tweets.  
Permite carregar dados em **CSV**, processar com **PySpark**, calcular polaridade com **TextBlob** e armazenar/analisar no **MySQL**.  

---

## Tecnologias utilizadas

- **Python 3.10+**
- **PySpark** (requer **Java JDK**)
- **TextBlob** (processamento de linguagem natural)
- **Pandas**
- **MySQL 8.x**
- **python-dotenv** (gerenciamento de variáveis de ambiente)

---

## Estrutura do projeto

```
Trabalho-Final-BD/
├─ data/                   # Coloque aqui os CSVs
│  ├─ Tweets.csv
│  └─ Tweets_10Milhao.csv  # Use o gerar_csv_grande.py para gerar esse arquivo
├─ src/
│  ├─ analise_mysql.py
│  ├─ analise_sentimento.py
│  ├─ carregar_dados_mysql.py
│  ├─ gerar_csv_grande.py
│  └─ test_conexao.py
├─ .env.example            # Modelo
└─ .gitignore
```

---

## Pré-requisitos

1. **Python 3.10+**  
   - Verifique: `python --version` ou `python3 --version`

2. **Java JDK 8+** (necessário para PySpark)  
   - Windows: instale [Adoptium Temurin](https://adoptium.net) (JDK 11 ou 17)  
   - macOS (Homebrew):  
     ```bash
     brew install temurin@17
     ```  
   - Linux:  
     ```bash
     sudo apt-get install -y default-jdk
     ```

3. **MySQL Server 8.x**  
   - Windows: instale pelo [MySQL Installer](https://dev.mysql.com/downloads/installer/)  
   - macOS:  
     ```bash
     brew install mysql
     brew services start mysql
     ```  
   - Linux:  
     ```bash
     sudo apt-get install -y mysql-server
     sudo systemctl enable --now mysql
     ```

---

## 🚀 Instalação do projeto

### Windows (PowerShell)
```powershell
git clone https://github.com/<seu-usuario>/Trabalho-Final-BD.git
cd Trabalho-Final-BD

python -m venv .venv
. .\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux
```bash
git clone https://github.com/<seu-usuario>/Trabalho-Final-BD.git
cd Trabalho-Final-BD

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuração do `.env`

O projeto utiliza variáveis de ambiente para escolher qual CSV usar e configurar o banco MySQL.  
Crie o `.env` a partir do modelo:

```bash
cp .env.example .env
```

### Exemplo de `.env`
```env
# Spark
SPARK_APP_NAME="Análise de Sentimentos - Projeto Final BDII"
INPUT_CSV_FILE="Tweets.csv"
# INPUT_CSV_FILE="Tweets_10Milhao.csv"

# MySQL
MYSQL_HOST="127.0.0.1"
MYSQL_PORT="3306"
MYSQL_USER="root"
MYSQL_PASSWORD="troque_aqui"
MYSQL_DATABASE="projeto_bd"
```

- Para rodar no dataset pequeno → `Tweets.csv`  
- Para rodar no dataset de 10 milhões → descomente a linha do `Tweets_10Milhao.csv` e comente a do `Tweets.csv`

---

## Configuração do MySQL

No MySQL, crie a base e tabela (ajuste conforme seu CSV):

```sql
CREATE DATABASE IF NOT EXISTS projeto_bd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS projeto_bd.tweets (
  id BIGINT PRIMARY KEY,
  text TEXT,
  created_at DATETIME NULL,
  user_id BIGINT NULL,
  user_name VARCHAR(255) NULL,
  sentimento VARCHAR(16) NULL
);
```

---

## Execução dos scripts

### 1) Testar conexão com MySQL
```bash
python src/test_conexao.py
```

---

### 2) Carregar CSV no MySQL
```bash
python src/carregar_dados_mysql.py
```
- Lê o arquivo definido em `INPUT_CSV_FILE` no `.env`
- Insere no banco definido em `MYSQL_DATABASE`

---

### 3) Rodar análise de sentimento com Spark
```bash
python src/analise_sentimento.py
```
- Usa `SPARK_APP_NAME` do `.env`  
- Aplica **TextBlob** para classificar tweets em `Positivo / Negativo / Neutro`  
- Pode gravar os resultados no banco MySQL

---

### 4) Consultas SQL no MySQL
```bash
python src/analise_mysql.py
```
Exemplo de SQL:
```sql
SELECT sentimento, COUNT(*) AS total
FROM tweets
GROUP BY sentimento
ORDER BY total DESC;
```

---

### 5) Gerar CSV sintético (teste local)
```bash
python src/gerar_csv_grande.py
```

---

## ⚠️ Informações/Dicas importantes

- **CSV muito grande?** → use o Spark (ele divide em partições automaticamente)  
- **Erro `ModuleNotFoundError: mysql`?** → instale `mysql-connector-python` (já no `requirements.txt`)  
- **Erro de Java?** → confirme que o JDK está instalado e no `PATH`  
- **Qualquer erro na instalação/configuração** → Abra um inssue

---
