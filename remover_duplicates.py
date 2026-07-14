import os
import re

PASTA = r"C:\Users\lucas.bezerra.NOVACASA\Desktop\imagem\imagens"

EXTENSOES = {".jpg", ".jpeg", ".png", ".webp"}

arquivos_existentes = {}

for nome in sorted(os.listdir(PASTA)):

    caminho = os.path.join(PASTA, nome)

    if not os.path.isfile(caminho):
        continue

    base, ext = os.path.splitext(nome)

    if ext.lower() not in EXTENSOES:
        print(f"Removendo arquivo não suportado: {nome}")
        os.remove(caminho)
        continue

    # Mantém apenas números
    numeros = re.sub(r"\D", "", base)

    if not numeros:
        print(f"Removendo sem código: {nome}")
        os.remove(caminho)
        continue

    # Remove zeros à esquerda
    novo_base = str(int(numeros))

    novo_nome = novo_base + ext.lower()
    novo_caminho = os.path.join(PASTA, novo_nome)

    # Se já existe, remove o duplicado
    if os.path.exists(novo_caminho) and os.path.abspath(caminho) != os.path.abspath(novo_caminho):
        print(f"Duplicado -> removendo {nome} (mantendo {novo_nome})")
        os.remove(caminho)
        continue

    # Renomeia se necessário
    if nome != novo_nome:
        print(f"Renomeando: {nome} -> {novo_nome}")
        os.rename(caminho, novo_caminho)

print("Concluído.")