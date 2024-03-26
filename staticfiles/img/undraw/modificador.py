import os
import re

# Diretório onde os arquivos SVG estão localizados
diretorio_svg = "/home/linux-senha-044119/Documentos/systempy/static/img/Undraw/"

# Cor a ser substituída
cor_antiga = "#1ec491"
cor_nova = "#0d1b2a"

# Lista para armazenar os arquivos SVG alterados
arquivos_alterados = []


# Função para substituir a cor em um arquivo SVG
def substituir_cor_em_arquivo(arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Substituir a cor antiga pela nova
        conteudo_modificado = re.sub(re.escape(cor_antiga), cor_nova, conteudo)

        # Escrever o conteúdo modificado de volta no arquivo
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo_modificado)

        arquivos_alterados.append(arquivo)
    except Exception as e:
        print(f"Erro ao processar o arquivo {arquivo}: {e}")


# Percorrer todos os arquivos no diretório
for raiz, diretorios, arquivos in os.walk(diretorio_svg):
    for arquivo in arquivos:
        if arquivo.endswith(".svg"):
            caminho_completo = os.path.join(raiz, arquivo)
            substituir_cor_em_arquivo(caminho_completo)

# Exibir a lista de arquivos SVG alterados
if arquivos_alterados:
    print("Alterações concluídas nos seguintes arquivos SVG:")
    for arquivo in arquivos_alterados:
        print(arquivo)
else:
    print("Nenhum arquivo SVG foi alterado.")
