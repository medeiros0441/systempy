from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from ..models.usuario import Usuario
from django.http import HttpResponse
from ..def_global import (
    criar_alerta_js,
    erro,
    email_existe,
    gerar_numero_aleatorio,
    usuario_existe,
)
from django.utils import timezone
from ..models.empresa import Empresa
from django.contrib.auth.hashers import make_password, check_password

from django.shortcuts import render
from ..models.usuario import Usuario


def listar_usuarios(request, alerta_js=None):
    id_empresa = request.session.get("id_empresa")
    usuarios = Usuario.objects.filter(empresa=id_empresa)
    context = {"usuarios": usuarios}

    if alerta_js:
        context["alerta_js"] = criar_alerta_js(alerta_js)

    return render(request, "usuario/lista_usuario.html", context)


# Detalhes de um usuário específico
def detalhes_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    data = {
        "id_usuario": usuario.id_usuario,
        "nome_completo": usuario.nome_completo,
        "nome_usuario": usuario.nome_usuario,
        "senha": usuario.senha,
        "data_insercao": usuario.data_insercao,
        "data_atualizacao": usuario.data_atualizacao,
        "nivel_usuario": usuario.nivel_usuario,
        "status": usuario.status,
        "email": usuario.email,
        "ultimo_login": usuario.ultimo_login,
    }
    return render(request, "usuario/select_usuario.html", {"data": data})


def cadastrar_usuario(request):
    caminho_html = "usuario/cadastro_usuario.html"

    if request.method == "POST":

        formulario = Usuario(
            nome_completo=request.POST.get("nome_completo"),
            senha=request.POST.get("senha"),
            nivel_usuario=int(request.POST.get("nivel_usuario")),
            status_acesso=bool(request.POST.get("status")),
            email=request.POST.get("email_responsavel"),
        )
        senha_hash = make_password(formulario.senha)

        verificacao = email_existe(formulario.email)
        if verificacao:
            return render(
                request,
                caminho_html,
                {
                    "alerta_js": criar_alerta_js(
                        "Email já está cadastro, coloque outro."
                    ),
                    "usuario": formulario,
                },
            )

        nome_usuario = formulario.nome_completo.replace(
            " ", ""
        ).lower()  # Remove espaços e converte para minúsculas
        # Se o nome de usuário já estiver em uso, adicionamos um número aleatório ao final
        nome_usuario
        usuario_existe(nome_usuario)
        while usuario_existe(nome_usuario):
            nome_usuario = nome_usuario + gerar_numero_aleatorio()

        id_empresa = request.session.get("id_empresa")

        # Verificar se os campos obrigatórios estão preenchidos
        if (
            formulario.nome_completo
            and nome_usuario
            and senha_hash
            and formulario.nivel_usuario
            and id_empresa
        ):
            try:
                # Converter id_empresa para inteiro
                id_empresa = int(id_empresa)

                # Obter a instância da empresa com base no id
                empresa = Empresa.objects.get(pk=id_empresa)

                # Verificar se id_usuario é zero antes de criar um novo usuário
                if empresa.id_empresa > 0:
                    # Criar um novo usuário com a instância da empresa
                    usuario_new = Usuario.objects.create(
                        nome_completo=formulario.nome_completo,
                        nome_usuario=nome_usuario,
                        senha=senha_hash,
                        nivel_usuario=int(formulario.nivel_usuario),
                        status_acesso=formulario.status_acesso,
                        email=formulario.email,
                        empresa=empresa,
                        insert=timezone.now(),
                    )
                    return redirect(
                        "listar_usuarios_alerta",
                        alerta_js="Usuário cadastrado com sucesso!",
                    )
            except Exception as e:
                mensagem_erro = str(e)
                return erro(request, mensagem_erro)
        else:
            return render(
                request,
                caminho_html,
                {"alerta": criar_alerta_js("erro ao recuperar dados.")},
            )
    else:
        return render(request, caminho_html)


from ..processador.config_email import enviar_email


def editar_usuario(request, id_usuario):
    caminho_html = "usuario/editar_usuario.html"
    if id_usuario > 0:
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        empresa_id = request.session.get("id_empresa")

        if request.method == "POST":

            nivel_usuario_str = request.POST.get("nivel_usuario")

            # Inicializa um valor padrão
            valor = 1

            # Verifica se nivel_usuario_str não é None e se é maior que 1
            if nivel_usuario_str is not None and int(nivel_usuario_str) > 1:
                valor = int(nivel_usuario_str)
            status_acesso_str = request.POST.get("status")
            if status_acesso_str is not None:
                status_acesso = bool(status_acesso_str)
            else:
                status_acesso = True
            # Cria o objeto do formulário
            formulario = Usuario(
                nome_completo=request.POST.get("nome_completo"),
                senha=request.POST.get("senha"),
                nivel_usuario=valor,
                status_acesso=status_acesso,
                email=request.POST.get("email_responsavel"),
            )
            # verificamos está em uso caso esteja.. verificamos se é
            # utilizado pelo usuario que está salvando os
            EmailisUtilizado = email_existe(formulario.email)
            if EmailisUtilizado:
                User = Usuario.objects.get(email=formulario.email)
                if User.id_usuario == usuario.id_usuario:
                    EmailisUtilizado = False

            # se o  email existir mas se for do usuario atual vamos ignorar o aviso de existencia
            if EmailisUtilizado == False:
                # caso o cliente tenha alterado o email vamos autenticar enviando um codigo para a confirmação
                ##se a sneha for alterada geremos a senha hash e
                # passamos para o model usuario para, a alterao
                if usuario.senha != formulario.senha:
                    senha_hash = make_password(formulario.senha)
                    usuario.senha = senha_hash

                if formulario.email != usuario.email:
                    assunto = "Email Alterado."
                    mensagem = f"Olá,{usuario.primeiro_nome}  Seu Email Alterado da plataforma SMW."
                    enviar_email(
                        destinatario=usuario.email,
                        assunto=assunto,
                        NomeCliente=usuario.primeiro_nome,
                        TextIntroducao=mensagem,
                    )
                    assunto = "Email inserido."
                    mensagem = f"Olá, {usuario.primeiro_nome} Seu Email foi inserido na plataforma SMW."
                    enviar_email(
                        destinatario=formulario.email,
                        assunto=assunto,
                        NomeCliente=usuario.primeiro_nome,
                        TextIntroducao=mensagem,
                    )
                    return render(
                        request,
                        caminho_html,
                        {
                            "alerta_js": criar_alerta_js(
                                "você alterou o email. foi enviado um codigo para a verificacão."
                            ),
                            "usuario": formulario,
                        },
                    )
                # Verifica se os campos obrigatórios estão preenchidos
                if formulario.nome_completo and formulario.nivel_usuario and empresa_id:
                    try:
                        usuario.nivel_usuario = int(formulario.nivel_usuario)
                        usuario.nome_completo = formulario.nome_completo
                        usuario.status_acesso = formulario.status_acesso
                        usuario.email = formulario.email
                        usuario.update = timezone.now()

                        usuario.save()
                        return redirect(
                            "listar_usuarios_alerta",
                            alerta_js="Usuário Editado com sucesso!",
                        )
                    except Exception as e:
                        mensagem_erro = str(e)
                        return erro(request, mensagem_erro)
            else:
                return render(
                    request,
                    caminho_html,
                    {
                        "alerta_js": criar_alerta_js(
                            "Email já está cadastro, coloque outro."
                        ),
                        "usuario": formulario,
                    },
                )
            # usuario nao é post. verifica se o id dele é o mesmo que o do usuario
        elif usuario.empresa.id_empresa == empresa_id:
            return render(request, caminho_html, {"usuario": usuario})
        else:  # Se o id do empresa não corresponder ao id do usuário,
            # retornar uma resposta de erro
            return render(
                "listar_usuario",
                {
                    "alerta_js": criar_alerta_js(
                        "Você não tem permissão para acessar este usuário."
                    )
                },
            )


from django.urls import reverse


def excluir_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id_usuario=id_usuario)
    if usuario:
        usuario.delete()
        return redirect(
            "listar_usuarios_alerta", alerta_js="Usuário excluído com sucesso!"
        )
    else:
        return redirect("listar_usuarios_alerta", alerta_js="Erro ao excluír Usuário!")


def bloquear_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id_usuario=id_usuario)
    usuario.status_acesso = False
    usuario.update = timezone.now()
    usuario.save()
    return redirect(
        "listar_usuarios_alerta", alerta_js="Usuário bloqueado com sucesso!"
    )


def ativar_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id_usuario=id_usuario)
    usuario.status_acesso = True
    usuario.update = timezone.now()
    usuario.save()
    return redirect("listar_usuarios_alerta", alerta_js="Usuário ativado com sucesso!")


def autenticar_usuario(email, senha):
    try:
        usuario = Usuario.objects.get(email=email)
        if check_password(senha, usuario.senha):
            return usuario
    except Usuario.DoesNotExist:
        pass
    return None
