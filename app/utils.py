from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .gerencia_email.config_email import enviar_email
from random import choices
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from functools import wraps
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from pytz import timezone
import random
import string

from app.static import UserInfo, Alerta


class Utils:
    @staticmethod
    def obter_data_hora_atual(brasil_date_only=False):
        # Obtém a data e hora atual no fuso horário do Brasil
        brasil_tz = timezone("America/Sao_Paulo")
        dt_brasil = datetime.now(brasil_tz)

        # Formata a data e hora de acordo com o parâmetro especificado
        if brasil_date_only:
            # Retorna apenas a data no formato dia/mes/ano
            return dt_brasil.strftime("%d/%m/%Y")
        else:
            # Retorna data e hora no formato dia/mes/ano hora:minutos
            return dt_brasil.strftime("%d/%m/%Y %H:%M")

    def criar_alerta_js(texto):
        # Modelo do script JavaScript que será retornado
        script = Utils.script_js(f"""  alertCustomer('{texto}');""")
        return script

    def script_js(function):
        # Modelo do script JavaScript que será retornado
        script = f"""
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                {function}
            }});
        </script>
        """
        return script

    def erro(request, error_message):
        if request.headers.get("Accept") == "application/json":
            # Se a solicitação aceitar JSON, retorne um JsonResponse com a mensagem de erro
            return JsonResponse({"error_message": error_message}, status=500)
        else:
            # Caso contrário, retorne o template HTML para exibir a mensagem de erro na página
            return render(request, "Erro.html", {"error_message": error_message})

    def gerar_numero_aleatorio(tamanho=4):
        # Gerar um número aleatório com 'tamanho' dígitos
        return "".join(random.choices(string.digits, k=tamanho))

    def email_existe(email):
        from app.models import Usuario

        return Usuario.objects.filter(email__iexact=email).exists()

    def usuario_existe(usuario):
        from app.models import Usuario

        return Usuario.objects.filter(nome_usuario__iexact=usuario).exists()

    def telefone_existe(telefone):
        from app.models import Empresa
        from app.models import Configuracao

        return Empresa.objects.filter(telefone__iexact=telefone).exists()

    def cpf_existe(cpf):
        from app.models import Empresa

        Empresa.objects.filter(nro_cpf__iexact=cpf).exists()
        return

    def cnpj_existe(cnpj):
        from app.models import Empresa

        return Empresa.objects.filter(nro_cnpj__iexact=cnpj).exists()

    @csrf_exempt
    def enviar_codigo(request, email):
        # Verificar o email e enviar o código
        enviado_com_sucesso, erro = Utils.verificar_email_e_enviar_codigo(
            request, email.lower()
        )

        # Verificar se o código foi enviado com sucesso
        if enviado_com_sucesso:
            return JsonResponse(
                {"success": "true", "mensagem": "Código enviado com sucesso!"}
            )
        else:
            # Verificar se o usuário não existe
            if erro == "usuario_nao_existe":
                return JsonResponse(
                    {"mensagem": "O usuário com o e-mail fornecido não existe."},
                )
            else:
                # Caso ocorra um erro genérico
                return JsonResponse(
                    {"erro": "Ocorreu um erro ao enviar o código."}, status=500
                )

    @csrf_exempt
    def confirmar_codigo(request, codigo):
        codigo_armazenado = request.session["codigo_senha_recuperacao"]
        if codigo_armazenado == codigo:
            return JsonResponse(
                {"success": "true", "mensagem": "Código confirmado com sucesso!"}
            )
        else:
            return JsonResponse({"mensagem": "Codigo Invalido"}, status=404)

    @csrf_exempt
    def atualizar_senha(request, nova_senha):
        status = Utils.RecuperacaoSenha(request, nova_senha)
        if status:
            return JsonResponse(
                {"success": "true", "mensagem": "Senha atualizada com sucesso!"}
            )
        else:
            return JsonResponse({"mensagem": "Erro interno Invalido"}, status=400)

    @csrf_exempt
    def verificar_email_e_enviar_codigo(request, email):
        from app.models import Usuario

        try:
            # Verificar se o usuário com o e-mail fornecido existe no banco de dados
            usuario = Usuario.objects.get(email=email)

            # Gerar um número com 6 dígitos
            codigo = (
                "".join(choices("0123456789", k=3))
                + "-"
                + "".join(choices("0123456789", k=3))
            )
            request.session["codigo_senha_recuperacao"] = codigo
            request.session["id_usuario"] = usuario.id_usuario

            # Enviar o código para o e-mail do usuário
            assunto = "Código de Recuperação de Senha"
            mensagem = f"Seu código de recuperação de senha é: {codigo}"
            enviar_email(
                destinatario=email,
                assunto=assunto,
                NomeCliente=usuario.primeiro_nome,
                TextIntroducao=mensagem,
            )

            # Retornar True para indicar que o código foi enviado com sucesso
            return True, None

        except ObjectDoesNotExist:
            # Lidar com o caso em que o usuário não existe
            # Por exemplo, você pode retornar False ou lançar uma exceção personalizada
            return False, "usuario_nao_existe"

        except Exception as e:
            # Lidar com outros erros inesperados
            print("Erro ao verificar e-mail e enviar código:", e)
            return False, "erro_interno"

    @csrf_exempt
    def RecuperacaoSenha(request, senha_nova):
        id = request.session["id_usuario"]
        from app.models import Usuario

        usuario = Usuario.objects.filter(id_usuario=id).first()
        if usuario:
            if senha_nova is None or senha_nova == "":
                return render(
                    request,
                    "default/login.html",
                    {
                        "alerta_js": Utils.criar_alerta_js("campo senha está vazio"),
                    },
                )

            else:
                senha_hash = make_password(senha_nova)
                usuario = Usuario.objects.get(id_usuario=id)
                usuario.senha = senha_hash
                usuario.save()
                request.session["senha_hash"] = senha_hash
                request.session["id_usuario"] = usuario.id_usuario

                assunto = "Senha Alterada."
                mensagem = f"Sua Senha foi  Alterado com Sucesso."
                enviar_email(
                    destinatario=usuario.email,
                    assunto=assunto,
                    NomeCliente=usuario.primeiro_nome,
                    TextIntroducao=mensagem,
                )
                return render(
                    request,
                    "default/login.html",
                    {
                        "alerta_js": Utils.criar_alerta_js(
                            "operação concluida com sucesso."
                        ),
                    },
                )
        return render(
            request,
            "default/login.html",
            {
                "alerta_js": Utils.criar_alerta_js("operação concluida com sucesso."),
            },
        )

    def get_status(request):
        from app.models import Usuario

        id_usuario = request.session.get("id_usuario")
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        return True

    def obter_dados_localizacao_ipinfo(ip, requests):
        # Chave de API do ipinfo.io
        api_key = "7a622c40229db0"

        # URL da API ipinfo.io
        url = f"http://ipinfo.io/{ip}?token={api_key}"

        try:
            # Fazendo uma solicitação GET para a API ipinfo.io
            response = requests.get(url)
            from app.models import Sessao

            # Verifica se a solicitação foi bem-sucedida (código de status HTTP 200)
            if response.status_code == 200:
                # Parseia os dados JSON da resposta
                data = response.json()
                sessao = Sessao.objects.create(
                    ip_sessao=ip,
                    cidade=data.get("city"),
                    regiao=data.get("region"),
                    pais=data.get("country"),
                    latitude=float(data.get("loc", "").split(",")[0]),
                    longitude=float(data.get("loc", "").split(",")[1]),
                    codigo_postal=data.get("postal"),
                    organizacao=data.get("org"),
                )

            else:
                # Se a solicitação falhar, imprime o status da resposta
                print(f"Erro: {response.status_code}")

        except Exception as e:
            print(f"Erro ao obter dados de localização: {e}")

    def configuracao_usuario(request, id_usuario, codigo):
        from app.view.views_erro import views_erro
        from app.models import Configuracao

        try:
            configuracao = Configuracao.objects.get(
                usuario_id=id_usuario, codigo=codigo
            )
            if not configuracao.status_acesso:
                mensagem = (
                    "Acesso negado: você não tem permissão para executar o método."
                )
                return False, views_erro.erro(request, mensagem)
            else:
                return True, None
        except ObjectDoesNotExist:
            mensagem = "Configuração não encontrada."
            return False, views_erro.erro(request, mensagem)
        except MultipleObjectsReturned:
            mensagem = "Ocorreu um erro inesperado. Por favor, entre em contato com a equipe de suporte."
            return False, views_erro.erro(request, mensagem)

    def verificar_permissoes(codigo_model):
        """
        Decorador para verificar as permissões do usuário antes de executar a função.
        """
        from .view.views_default import views_default as default

        def decorator(func):
            @wraps(func)
            def wrapper(request, *args, **kwargs):
                # Obtém o ID do usuário da requisição
                id_empresa = UserInfo.get_id_empresa(request)
                id_usuario = UserInfo.get_id_usuario(request)
                if id_usuario == 0 or id_empresa == 0:
                    type = default.login(request, {"set_autenticacao": True})
                    if type != True:
                        Alerta.set_mensagem(
                            "Se você deseja continuar, é necessário estar logado"
                        )
                        return type

                # Verifica as permissões do usuário com base no código
                status, render = Utils.configuracao_usuario(
                    request, id_usuario, codigo_model
                )
                if status:
                    return func(request, *args, **kwargs)
                else:
                    return render

            return wrapper

        return decorator

    def lista_de_configuracao():
        return [
            {"nome": "Usuario", "codigo": 1},
            {"nome": "Empresa", "codigo": 2},
            {"nome": "Endereco", "codigo": 3},
            {"nome": "Galao", "codigo": 4},
            {"nome": "Loja", "codigo": 5},
            {"nome": "Produto", "codigo": 6},
            {"nome": "Venda", "codigo": 7},
            {"nome": "Cliente", "codigo": 8},
            {"nome": "Motoboy", "codigo": 9},
            {"nome": "Caixa", "codigo": 10},
            {"nome": "Transacao", "codigo": 11},
            {"nome": "Faturamento", "codigo": 12},
        ]

    def buscar_codigo_por_nome(nome_classe):
        for configuracao in Utils.lista_de_configuracao():
            if configuracao["nome"] == nome_classe:
                return configuracao["codigo"]
        return None

    def buscar_nome_por_codigo(codigo_classe):
        for configuracao in Utils.lista_de_configuracao():
            if configuracao["codigo"] == codigo_classe:
                return configuracao["nome"]
        return None
