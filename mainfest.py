import json
from pathlib import Path

# Caminho da pasta onde estão as imagens
PASTA_IMAGENS = Path("imagens")

# Arquivo que será gerado
MANIFEST = Path("manifest.json")

USUARIO = "filesarquivos3-dev"
REPOSITORIO = "imagens"
BRANCH = "main"

EXTENSOES = {".jpg", ".jpeg", ".png", ".webp"}

manifest = []

for arquivo in PASTA_IMAGENS.rglob("*"):

    if arquivo.suffix.lower() not in EXTENSOES:
        continue

    caminho = arquivo.as_posix()

    manifest.append({
        "sku": arquivo.stem,
        "arquivo": caminho,
        "url": (
            f"https://raw.githubusercontent.com/"
            f"{USUARIO}/{REPOSITORIO}/{BRANCH}/{caminho}"
        )
    })

# Ordena pelo SKU
manifest.sort(key=lambda x: x["sku"])

with open(MANIFEST, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Manifest criado com {len(manifest)} imagens.")