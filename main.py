import os
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import requests

from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DBNAME')}?sslmode=require"
)


GITHUB_USUARIO = "filesarquivos3-dev"
GITHUB_REPO = "imagens_db"
GITHUB_BRANCH = "main"

EXTENSOES_VALIDAS = (".jpg", ".jpeg", ".png", ".webp")


MANIFEST_URL = (
    "https://raw.githubusercontent.com/"
    "filesarquivos3-dev/imagens_db/main/manifest.json"
)

response = requests.get(MANIFEST_URL)
response.raise_for_status()

df = pd.DataFrame(response.json())

# Renomeia para bater com a tabela
df = df.rename(columns={"sku": "codproduto"})

# Mantém apenas as colunas necessárias
df = df[["codproduto", "url"]]

print(df.head())
print(f"Encontradas {len(df)} imagens.")

from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text("""
        TRUNCATE TABLE pricing.imagem_produto RESTART IDENTITY;
    """))

df.to_sql(
    name="imagem_produto",
    schema="pricing",
    con=engine,
    if_exists="append",
    index=False
)

print(f"{len(df)} registros gravados.")