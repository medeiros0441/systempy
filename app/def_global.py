from django.shortcuts import render, redirect
from .models import Empresa, Usuario, Configuracao
from django.contrib.auth.hashers import check_password, make_password
from .processador.config_email import enviar_email
from random import choices
from django.core.exceptions import ObjectDoesNotExist
import random
import string


def criar_alerta_js(texto):
    # Modelo do script JavaScript que será retornado
    script = script_js(f"""  alertCustomer('{texto}');""")
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


from django.http import JsonResponse


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
    return Usuario.objects.filter(email__iexact=email).exists()


def usuario_existe(usuario):
    return Usuario.objects.filter(nome_usuario__iexact=usuario).exists()


def telefone_existe(telefone):
    return Empresa.objects.filter(telefone__iexact=telefone).exists()


def cpf_existe(cpf):
    Empresa.objects.filter(nro_cpf__iexact=cpf).exists()
    return


def cnpj_existe(cnpj):
    return Empresa.objects.filter(nro_cnpj__iexact=cnpj).exists()


from django.http import JsonResponse


def enviar_codigo(request, email):
    enviado_com_sucesso, erro = verificar_email_e_enviar_codigo(request, email)

    if enviado_com_sucesso:
        return JsonResponse({"mensagem": "Código enviado com sucesso!"})
    else:
        if erro == "usuario_nao_existe":
            return JsonResponse(
                {"erro": "O usuário com o e-mail fornecido não existe."}, status=404
            )
        else:
            return JsonResponse(
                {"erro": "Ocorreu um erro ao enviar o código."}, status=500
            )


def confirmar_codigo(request, codigo):
    codigo_armazenado = request.session["codigo_senha_recuperacao"]
    if codigo_armazenado == codigo:
        return JsonResponse({"mensagem": "Código confirmado com sucesso!"})
    else:
        return JsonResponse({"erro": "Codigo Invalido"}, status=404)


def atualizar_senha(request, nova_senha):
    status = RecuperacaoSenha(request, nova_senha)
    if status:
        return JsonResponse({"mensagem": "Senha atualizada com sucesso!"})
    else:
        return JsonResponse({"erro": "Erro interno Invalido"}, status=400)


def verificar_email_e_enviar_codigo(request, email):

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


def RecuperacaoSenha(request, senha_nova):
    id = request.session["id_usuario"]
    usuario = Usuario.objects.filter(id_usuario=id).first()
    if usuario:
        if senha_nova is None or senha_nova == "":
            return render(
                request,
                "default/login.html",
                {
                    "alerta_js": criar_alerta_js("campo senha está vazio"),
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
                    "alerta_js": criar_alerta_js("operação concluida com sucesso."),
                },
            )
    return render(
        request,
        "default/login.html",
        {
            "alerta_js": criar_alerta_js("operação concluida com sucesso."),
        },
    )


def get_status(request):
    id_usuario = request.session.get("id_usuario")
    usuario = Usuario.objects.get(id_usuario=id_usuario)

    return True


from .models import Sessao


def obter_dados_localizacao_ipinfo(ip, requests):
    # Chave de API do ipinfo.io
    api_key = "7a622c40229db0"

    # URL da API ipinfo.io
    url = f"http://ipinfo.io/{ip}?token={api_key}"

    try:
        # Fazendo uma solicitação GET para a API ipinfo.io
        response = requests.get(url)

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


from functools import wraps
from .static import UserInfo, Alerta
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def verificar_permissoes(codigo_model):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            id_usuario = UserInfo.get_id_usuario(request)
            try:
                configuracao = Configuracao.objects.get(
                    usuario_id=id_usuario, codigo=codigo_model
                )
                if not configuracao.status_acesso:
                    Alerta.set_mensagem(
                        "Acesso negado: você não tem permissão para executar o método."
                    )
                    return erro(
                        request,
                        "Acesso negado: você não tem permissão para executar o método.",
                    )
            except Configuracao.DoesNotExist:
                Alerta.set_mensagem("Configuração não encontrada.")
                return erro(request, "Configuração não encontrada.")
            except MultipleObjectsReturned:
                Alerta.set_mensagem(
                    "Ocorreu um erro inesperado. Por favor, entre em contato com a equipe de suporte."
                )
                return erro(
                    request,
                    "Ocorreu um erro inesperado. Por favor, entre em contato com a equipe de suporte.",
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
