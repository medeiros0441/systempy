from django.shortcuts import render, redirect
from ..models import Empresa, Usuario
from ..utils import utils
import json
from django.contrib.auth.hashers import make_password
from ..static import Alerta, UserInfo
from .views_configuracao import views_configuracao
from .views_autenticacao import views_autenticacao

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class views_cadastro:

    def validacao(campos):
        mensagens_alerta = []

        def verificar_existencia(campo, valor, funcao_verificadora):
            if funcao_verificadora(valor):
                mensagens_alerta.append(f"{campo} já cadastrado.")

        for campo, valor in campos.items():
            if campo == "E-mail":
                verificar_existencia(campo, valor, utils.email_existe)
            elif campo == "Telefone":
                verificar_existencia(campo, valor, utils.telefone_existe)
            elif campo == "CPF":
                verificar_existencia(campo, valor, utils.cpf_existe)
            elif campo == "CNPJ":
                verificar_existencia(campo, valor, utils.cnpj_existe)

        texto_alerta = "\n".join(mensagens_alerta)
        return texto_alerta.replace("\n", "\\n")  # Substituir quebras de linha por '\n'

    @csrf_exempt
    def cadastro_empresa(request):
        try:
            if request.method == "POST":
                data = json.loads(request.body)

                email_responsavel = data.get("email_responsavel", "").lower().strip()
                dados_formulario = {
                    "nome_empresa": data.get("nome_empresa"),
                    "nro_cnpj": data.get("nro_cnpj"),
                    "razao_social": data.get("razao_social_empresa"),
                    "descricao": data.get("descricao_empresa"),
                    "nome_responsavel": data.get("nome_responsavel"),
                    "cargo": data.get("cargo_responsavel"),
                    "email": email_responsavel,
                    "nro_cpf": data.get("nro_cpf"),
                    "telefone": data.get("telefone_responsavel"),
                }
                mensagens_alerta = []

                campos = {
                    "E-mail": email_responsavel,
                    "Telefone": dados_formulario.get("telefone"),
                    "CPF": dados_formulario.get("nro_cpf"),
                    "CNPJ": dados_formulario.get("nro_cnpj"),
                }

                mensagens_alerta = views_cadastro.validacao(campos)
                if mensagens_alerta:
                    return JsonResponse(
                        {"success": False, "messages": mensagens_alerta}, status=400
                    )

                senha = data.get("senha")
                if not senha:
                    return JsonResponse(
                        {"success": False, "messages": ["Campo senha está vazio"]},
                        status=400,
                    )

                senha_hash = make_password(senha)
                empresa = views_cadastro.criar_empresa(dados_formulario)
                if empresa:
                    string_value = views_cadastro.criar_user(empresa, senha_hash)
                    if string_value is True:
                        if views_autenticacao.autenticar_usuario(request, email_responsavel, senha):
                            return JsonResponse(
                                {"success": True, "redirect": "dashbord"}
                            )
                        else:
                            return JsonResponse({"success": True, "redirect": "login"})
                    else:
                        return JsonResponse(
                            {"success": False, "messages": [string_value]}, status=400
                        )
                else:
                    return JsonResponse(
                        {"success": False, "messages": ["Erro ao criar empresa"]},
                        status=400,
                    )
            else:
                return JsonResponse(
                    {"success": False, "messages": ["Método não permitido"]}, status=405
                )
        except Exception as e:
            return JsonResponse({"success": False, "messages": [str(e)]}, status=500)

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
            numero_aleatorio = utils.gerar_numero_aleatorio()
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
            list = views_configuracao.list_configuracoes_padrao(novo_usuario)
            views_configuracao.criar_configuracoes_padrao(list)
            return True
        except Exception as e:
            mensagem_erro = str(e)
            print(
                "Erro ao criar usuário:", mensagem_erro
            )  # Adiciona mensagem de depuração
            return mensagem_erro
