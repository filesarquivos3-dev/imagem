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
GITHUB_REPO = "imagem"
GITHUB_BRANCH = "main"

EXTENSOES_VALIDAS = (".jpg", ".jpeg", ".png", ".webp")


MANIFEST_URL = (
    "https://raw.githubusercontent.com/"
    "filesarquivos3-dev/imagem/main/manifest.json"
)

response = requests.get(MANIFEST_URL)
response.raise_for_status()

df = pd.DataFrame(response.json())

# Renomeia para bater com a tabela
df = df.rename(columns={"sku": "codproduto"})

# Extrai a extensão da URL
df["extensao"] = df["url"].apply(lambda x: os.path.splitext(x)[1].lower())

# Prioridade das extensões
prioridade = {
    ".jpg": 1,
    ".jpeg": 2,
    ".png": 3,
    ".webp": 4
}

df["prioridade"] = df["extensao"].map(prioridade).fillna(99)

# Ordena pela prioridade
df = df.sort_values(["codproduto", "prioridade"])

# Mantém apenas a melhor imagem de cada produto
duplicados = df[df.duplicated("codproduto", keep=False)]

if not duplicados.empty:
    print("\nProdutos com mais de uma imagem:")
    print(duplicados[["codproduto", "url"]].to_string(index=False))

df = df.drop_duplicates(subset="codproduto", keep="first")

# Remove colunas auxiliares
df = df[["codproduto", "url"]]

print(f"Total após remover duplicados: {len(df)}")




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