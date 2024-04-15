from django.shortcuts import render, redirect
from ..models.usuario import Usuario
from ..models.empresa import Empresa
from ..def_global import (
    criar_alerta_js,
    erro,
    email_existe,
    telefone_existe,
    cpf_existe,
    cnpj_existe,
    gerar_numero_aleatorio,
)
from django.utils import timezone

from django.contrib.auth.hashers import make_password
from ..static import Alerta, UserInfo


def validacao(campos):
    mensagens_alerta = []

    def verificar_existencia(campo, valor, funcao_verificadora):
        if funcao_verificadora(valor):
            mensagens_alerta.append(f"{campo} já cadastrado.")

    for campo, valor in campos.items():
        if campo == "E-mail":
            verificar_existencia(campo, valor, email_existe)
        elif campo == "Telefone":
            verificar_existencia(campo, valor, telefone_existe)
        elif campo == "CPF":
            verificar_existencia(campo, valor, cpf_existe)
        elif campo == "CNPJ":
            verificar_existencia(campo, valor, cnpj_existe)

    texto_alerta = "\n".join(mensagens_alerta)
    return texto_alerta.replace("\n", "\\n")  # Substituir quebras de linha por '\n'


from .view_configuracao import criar_configuracoes_padrao, list_configuracoes_padrao


def cadastro_empresa(request):
    try:
        if request.method == "POST":
            dados_formulario = {
                "nome_empresa": request.POST.get("nome_empresa"),
                "nro_cnpj": request.POST.get("nro_cnpj"),
                "razao_social": request.POST.get("razao_social_empresa", ""),
                "descricao": request.POST.get("descricao_empresa"),
                "nome_responsavel": request.POST.get("nome_responsavel"),
                "cargo": request.POST.get("cargo_responsavel"),
                "email": request.POST.get("email_responsavel"),
                "nro_cpf": request.POST.get("nro_cpf"),
                "telefone": request.POST.get("telefone_responsavel"),
            }
            mensagens_alerta = []

            campos = {
                "E-mail": dados_formulario.get("email_responsavel").lower(),
                "Telefone": dados_formulario.get("telefone_responsavel"),
                "CPF": dados_formulario.get("nro_cpf_responsavel"),
                "CNPJ": dados_formulario.get("nro_cnpj"),
            }
            mensagens_alerta = validacao(campos)
            if mensagens_alerta:
                return render(
                    request,
                    "default/cadastro.html",
                    {
                        "alerta_js": criar_alerta_js(mensagens_alerta),
                        **dados_formulario,
                    },
                )
            empresa = criar_empresa(dados_formulario)
            senha = request.POST.get("senha")

            senha_hash = make_password(senha)

            if senha is None or senha == "":
                return render(
                    request,
                    "default/cadastro.html",
                    {
                        "alerta_js": criar_alerta_js("campo senha está vazio"),
                        **dados_formulario,
                    },
                )
            elif empresa:
                string_value = criar_user(empresa, senha_hash)
                if string_value is True:
                    
                    return redirect("login")
                else:
                    # Se não foi possível criar o usuário, exiba uma mensagem de erro na tela
                    return erro(request, string_value)

        else:
            return render(request, "default/cadastro.html")

    except Exception as e:
        mensagem_erro = str(e)
        return erro(request, mensagem_erro)


def criar_empresa(dados_empresa):
    try:
        nova_empresa = Empresa.objects.create(**dados_empresa)
        print(nova_empresa)
        return nova_empresa
    except Exception as e:
        mensagem_erro = str(e)
        return mensagem_erro


def criar_user(empresa, senha):
    # Criação do novo usuário associado à empresa
    # Retorna True se o usuário foi criado com sucesso, False caso contrário
    try:
        numero_aleatorio = gerar_numero_aleatorio()
        novo_nome_usuario = empresa.nome_responsavel + numero_aleatorio

        # Criando o novo usuário associado à empresa
        novo_usuario = Usuario.objects.create(
            nome_completo=empresa.nome_responsavel,
            nome_usuario=novo_nome_usuario,
            senha=senha,
            nivel_usuario=1,
            status_acesso=True,
            email=empresa.email,
            empresa=empresa,
        )
        list = list_configuracoes_padrao(novo_usuario)
        criar_configuracoes_padrao(list)
        return True
    except Exception as e:
        mensagem_erro = str(e)
        print("Erro ao criar usuário:", mensagem_erro)  # Adiciona mensagem de depuração
        return mensagem_erro
