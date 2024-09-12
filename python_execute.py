import os

# Diretório onde os arquivos de interface serão criados
interface_dir = 'frontend/src/interface/'

# Lista de serializers mencionados no __all__
serializers = [
    "ClienteSerializer",
    "EntregaSerializer",
    "LogSerializer",
    "CustomModelSerializer",
    "GalaoSerializer",
    "LojaSerializer",
    "SessaoSerializer",
    "EmpresaSerializer",
    "HistoricoSerializer",
    "PdvSerializer",
    "UsuarioSerializer",
    "EnderecoSerializer",
    "ProdutoSerializer",
    "VendaSerializer",
    "MotoboySerializer"
]

# Verificando se o diretório de interface existe, senão cria
if not os.path.exists(interface_dir):
    os.makedirs(interface_dir)

# Iterando sobre os serializers e criando arquivos de interface se não existirem
for serializer in serializers:
    model_name = serializer.replace('Serializer', 'Interface')
    file_path = os.path.join(interface_dir, f"{model_name}.jsx")

    # Criando arquivo apenas se ele não existir
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass  # Criando o arquivo vazio
        print(f"Arquivo {file_path} criado com sucesso.")
    else:
        print(f"Arquivo {file_path} já existe, pulando...")

print("Finalizado.")
