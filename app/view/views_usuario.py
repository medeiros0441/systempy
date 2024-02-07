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

from django.contrib.auth.hashers import make_password, check_password


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(
        request, "cliente/usuario/listar_usuario.html", {"usuarios": usuarios}
    )


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
    return render(request, "cliente/usuario/select_usuario.html", {"data": data})


def cadastrar_usuario(request, id_usuario=0):
    caminho_html = "cliente/usuario/cadastro_usuario.html"

    if request.method == "POST":
        nome_completo = request.POST.get("nome_completo")
        senha_digitada = request.POST.get("senha")
        senha_hash = make_password(senha_digitada)
        nivel_usuario = request.POST.get("nivel_usuario")
        status = request.POST.get("status")
        email = request.POST.get("email_responsavel")
        verificacao = email_existe(email)
        if verificacao:
            return render(
                request,
                caminho_html,
                {
                    "alerta_js": criar_alerta_js(
                        "Email já está cadastro, coloque outro."
                    )
                },
            )

        nome_usuario = nome_completo.replace(
            " ", ""
        ).lower()  # Remove espaços e converte para minúsculas
        # Se o nome de usuário já estiver em uso, adicionamos um número aleatório ao final
        verificar_uso = usuario_existe(nome_usuario)
        while verificar_uso:
            nome_usuario + gerar_numero_aleatorio()

        id_empresa = request.session.get("id_empresa")

        # Verifica se os campos obrigatórios estão preenchidos
        if (
            nome_completo
            and nome_usuario
            and senha_hash
            and nivel_usuario
            and id_empresa
        ):
            try:
                fk_empresa = int(id_empresa)
                nivel_usuario = int(nivel_usuario)

                if id_usuario == 0:
                    usuario = Usuario.objects.create(
                        nome_completo=nome_completo,
                        nome_usuario=nome_usuario,
                        senha=senha_hash,
                        nivel_usuario=nivel_usuario,
                        status=status,
                        email=email,
                        fk_empresa=fk_empresa,
                    )
                    return redirect(
                        request,
                        "listar_usuario",
                        {"alerta": criar_alerta_js("Usuario cadastrado.")},
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


def editar_usuario(request, id_usuario):
    caminho_html = "cliente/usario/cadastro_usuario.html"
    if id_usuario > 0:
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        fk_empresa_id = request.session.get("id_empresa")
        if request.method == "POST":
            nome_completo = request.POST.get("nome_completo")
            nivel_usuario = request.POST.get("nivel_usuario")
            status = request.POST.get("status")
            email = request.POST.get("email_responsavel")
            if email != usuario.email:
                verificacao = email_existe(email)
                if verificacao:
                    return render(
                        request,
                        caminho_html,
                        {
                            "alerta_js": criar_alerta_js(
                                "Email já está cadastro, coloque outro."
                            )
                        },
                    )
                fk_empresa_id = request.session.get("id_empresa")
                # Verifica se os campos obrigatórios estão preenchidos
                if nome_completo and nivel_usuario and fk_empresa_id:
                    try:
                        fk_empresa_id = int(fk_empresa_id)
                        nivel_usuario = int(nivel_usuario)
                        usuario.nome_completo = (nome_completo,)
                        usuario.nivel_usuario = (nivel_usuario,)
                        usuario.status = (status,)
                        usuario.email = (email,)
                        usuario.empresa = (fk_empresa_id,)
                        usuario.data_atualizacao = timezone.now()
                        usuario.save()
                        return redirect(
                            request,
                            "listar_usuario",
                            {"alerta": criar_alerta_js("Usuario Atualizado.")},
                        )
                    except Exception as e:
                        mensagem_erro = str(e)
                        return erro(request, mensagem_erro)

                if usuario.fk_empresa.id_empresa == fk_empresa_id:
                    return render(request, caminho_html, {"usuario": usuario})
        else:
            # Se o id do cliente não corresponder ao id do usuário,
            # retornar uma resposta de erro
            return render(
                "listar_usuario",
                {
                    "alerta_js": criar_alerta_js(
                        "Você não tem permissão para acessar este usuário."
                    )
                },
            )


@csrf_exempt
def excluir_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)

    if request.method == "DELETE":
        usuario.delete()
        return JsonResponse({"mensagem": "Usuário excluído com sucesso!"})
    else:
        return JsonResponse({"mensagem": "Método não permitido"}, status=405)


def bloquear_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id_usuario=id_usuario)
    usuario.status = "Bloqueado"
    usuario.save()
    return redirect(
        request,
        "cliente/usuario/listar_usuarios",
        {"alerta_js": criar_alerta_js("Usuario Bloquado.")},
    )


def ativar_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.status = "Ativo"
    usuario.save()
    return redirect(
        request,
        "cliente/usuario/listar_usuarios",
        {"alerta_js": criar_alerta_js("Usuario Ativo.")},
    )


def autenticar_usuario(email, senha):
    try:
        usuario = Usuario.objects.get(email=email)
        if check_password(senha, usuario.senha):
            return usuario
    except Usuario.DoesNotExist:
        pass
    return None
