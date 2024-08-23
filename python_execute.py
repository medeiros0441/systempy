import os
import re

# Caminho para o diretório onde estão os models
models_dir = 'api/models/'

# Função para processar cada arquivo e remover a classe Meta incorreta
def remove_incorrect_meta(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    skip_lines = False

    for i, line in enumerate(lines):
        # Detecta a linha com a definição da classe Meta incorreta
        if re.match(r'^\s*class Meta:\s*$', line):
            # Verifica se a próxima linha define db_table
            if re.match(r"^\s*db_table = '.*'\s*$", lines[i + 1]):
                # Pular as próximas 2 linhas: `class Meta:` e `db_table = '...'`
                skip_lines = True
                continue

        # Se estiver no modo de pular linhas, salta a próxima linha
        if skip_lines:
            if re.match(r'^\s*$', line):
                skip_lines = False
            continue

        # Adiciona a linha atual às linhas atualizadas
        updated_lines.append(line)

    # Escreve as linhas atualizadas de volta ao arquivo
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

# Função para percorrer todos os arquivos do diretório models
def process_models_directory(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                remove_incorrect_meta(file_path)

# Executa o script
process_models_directory(models_dir)

print("Processo de remoção concluído!")
