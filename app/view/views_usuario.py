from django.shortcuts import render, redirect, get_object_or_404
from ..def_global import (
    criar_alerta_js,
    erro,
    email_existe,
    gerar_numero_aleatorio,
    usuario_existe,
)
from ..static import Alerta, UserInfo
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from ..models import Usuario, Empresa


def listar_usuarios(request, context=None):
    id_empresa = UserInfo.get_id_empresa(request)

    usuarios = Usuario.objects.filter(empresa=id_empresa)
    if context is None:
        context = {}
    context["usuarios"] = usuarios
    alerta_js = Alerta.get_mensagem()
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
        "data_insercao": usuario.insert,
        "data_atualizacao": usuario.update,
        "nivel_usuario": usuario.nivel_usuario,
        "status": usuario.status_acesso,
        "email": usuario.email,
        "ultimo_login": usuario.ultimo_login,
    }
    return render(request, "usuario/select_usuario.html", {"data": data})


from .view_configuracao import criar_configuracoes_padrao
from ..models import Configuracao


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
                    criar_configuracoes_padrao(usuario_new)
                    Alerta.set_mensagem("Usuário cadastrado com sucesso!")
                    return redirect(
                        "listar_usuarios",
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
        list = list_configuracoes_padrao2()
        return render(request, caminho_html, {"list_configuracao": list})


def list_configuracoes_padrao2():

    nomes_classes = [
        "Usuario",
        "Empresa",
        "Endereco",
        "Galao",
        "Loja",
        "Produto",
        "Sessao",
        "Venda",
        "Historico",
        "Log",
        "Configuracao",
        "Cliente",
    ]

    list_configuracao = []

    for nome_classe in nomes_classes:
        titulo = f"Gerenciamento de {nome_classe}"
        descricao_interna = (
            f"Controle de {nome_classe.lower()}, editar, alterar, criar..."
        )
        descricao = f"Permitir acesso ao Painel de {nome_classe}, isso inclui criar, editar, remover, entre outros."
        status_acesso = False
        configuracao = Configuracao(
            titulo=titulo,
            descricao_interna=descricao_interna,
            descricao=descricao,
            status_acesso=status_acesso,
        )
        list_configuracao.append(configuracao)

    return list_configuracao


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
                nivel_usuario=valor,
                status_acesso=status_acesso,
            )
            # Verifica se os campos obrigatórios estão preenchidos
            if formulario.nome_completo and formulario.nivel_usuario and empresa_id:
                try:
                    usuario.nivel_usuario = int(formulario.nivel_usuario)
                    usuario.nome_completo = formulario.nome_completo
                    usuario.status_acesso = formulario.status_acesso
                    usuario.update = timezone.now()
                    usuario.save()
                    Alerta.set_mensagem("Usuário Editado com sucesso!")
                    return redirect(
                        "listar_usuarios",
                    )
                except Exception as e:
                    mensagem_erro = str(e)
                    return erro(request, mensagem_erro)
            # usuario nao é post. verifica se o id dele é o mesmo que o do usuario
        elif usuario.empresa.id_empresa == empresa_id:
            return render(request, caminho_html, {"usuario": usuario})
        else:  # Se o id do empresa não corresponder ao id do usuário,
            Alerta.set_mensagem("Você não tem permissão para acessar este usuário.")
            return redirect(
                "listar_usuarios",
            )


from django.urls import reverse


def excluir_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id_usuario=id_usuario)
    if usuario:
        usuario.delete()
        Alerta.set_mensagem("Usuário excluído com sucesso!")
        return redirect(
            "listar_usuarios",
        )
    else:
        Alerta.set_mensagem("Erro ao excluír Usuário!")
        return redirect(
            "listar_usuarios",
        )


def bloquear_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id_usuario=id_usuario)
    usuario.status_acesso = False
    usuario.update = timezone.now()
    usuario.save()

    Alerta.set_mensagem("Usuário bloqueado com sucesso!")
    return redirect(
        "listar_usuarios",
    )


def ativar_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id_usuario=id_usuario)
    usuario.status_acesso = True
    usuario.update = timezone.now()
    usuario.save()
    Alerta.set_mensagem("Usuário ativado com sucesso!")
    return redirect(
        "listar_usuarios",
    )


def autenticar_usuario(email, senha):
    try:
        usuario = Usuario.objects.get(email__iexact=email)
        if check_password(senha, usuario.senha):
            return usuario
    except Usuario.DoesNotExist:
        pass
    return None
