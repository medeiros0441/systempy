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
from ..models import Usuario, Configuracao, Loja, Associado
from .view_configuracao import criar_configuracoes_padrao, list_configuracoes_padrao
from ..forms import UsuarioForm
from functools import wraps


def verificar_permissoes(codigo_model):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            id_usuario = UserInfo.get_id_usuario(request)
            try:
                configuracao = Configuracao.objects.get(
                    usuario_id=id_usuario, codigo=codigo_model
                )
                if configuracao.status_acesso == False:
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
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


class view_usuarios:

    @staticmethod
    @verificar_permissoes(codigo_model=1)
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

    @staticmethod
    @verificar_permissoes(codigo_model=1)
    def detalhes_usuario(request, id_usuario):
        usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        associados = Associado.objects.filter(usuario=usuario)

        associados_list = []
        for associado in associados:
            status = "Autorizado" if associado.status_acesso else "Não Permitido"
            associados_list.append(
                {
                    "status": status,
                    "nome": associado.loja.nome_loja,
                    "atualizado": associado.update,
                }
            )

        return view_usuarios.listar_usuarios(
            request,
            {
                "open_modal": True,
                "text_usuario": usuario,
                "associados_list": associados_list,
            },
        )

    @staticmethod
    @verificar_permissoes(codigo_model=1)
    def editar_usuario(request, id_usuario):
        try:
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            id_empresa = UserInfo.get_id_empresa(request)
            list_lojas = Loja.objects.filter(empresa_id=id_empresa)

            if request.method == "POST":
                usuario.nome_completo = request.POST["nome_completo"]
                if usuario.nivel_usuario > 1:
                    usuario.nivel_usuario = request.POST["nivel_usuario"]
                    usuario.status_acesso = request.POST["status_acesso"]
                if usuario.nome_completo:

                    usuario.update = timezone.now()
                    usuario.save()
                    for loja in list_lojas:
                        campo_checkbox = f"status_acesso_{loja.id_loja}"
                        associacao, created = Associado.objects.get_or_create(
                            usuario_id=id_usuario,
                            loja_id=loja.id_loja,
                            defaults={'status_acesso': campo_checkbox in request.POST, 'update': timezone.now()}
                        )
                        if not created:
                            associacao.status_acesso = campo_checkbox in request.POST
                            associacao.update = timezone.now()
                            associacao.save()
                    Alerta.set_mensagem("Usuário editado com sucesso!")
                    return redirect("listar_usuarios")
                else:
                    Alerta.set_mensagem(
                        "Formulário inválido. Por favor, corrija os erros."
                    )
            else:
                form_usuario = UsuarioForm(instance=usuario)

                list_objs = []

                associado = Associado.objects.filter(usuario=usuario)

                for loja in list_lojas:
                    loja_info = {
                        "id_loja": loja.id_loja,  # ID da loja
                        "nome_loja": loja.nome_loja,  # Nome da loja (suponha que o campo no modelo seja 'nome')
                        "status_acesso": False,  # Status de acesso padrão, inicialmente definido como False
                    }
                    associado_loja = associado.filter(loja_id=loja.id_loja).first()
                    if associado_loja:
                        loja_info["status_acesso"] = associado_loja.status_acesso

                    list_objs.append(loja_info)
                return view_usuarios.listar_usuarios(
                    request,
                    {
                        "form_usuario": form_usuario,
                        "list_lojas": list_objs,
                        "open_modal": True,
                        "isEditar": True,
                    },
                )
        except Associado.DoesNotExist:
            pass
        except Loja.DoesNotExist:
            pass
        Alerta.set_mensagem("Para associar um usuario a loja, precisa criar uma!")
        form_usuario = UsuarioForm(instance=usuario)
        return view_usuarios.listar_usuarios(
            request,
            {
                "form_usuario": form_usuario,
                "open_modal": True,
                "isEditar": True,
            },
        )

    @staticmethod
    @verificar_permissoes(codigo_model=1)
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

    @staticmethod
    @verificar_permissoes(codigo_model=1)
    def bloquear_usuario(request, id_usuario):
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        usuario.status_acesso = False
        usuario.update = timezone.now()
        usuario.save()

        Alerta.set_mensagem("Usuário bloqueado com sucesso!")
        return redirect(
            "listar_usuarios",
        )

    @staticmethod
    @verificar_permissoes(codigo_model=1)
    def ativar_usuario(request, id_usuario):
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        usuario.status_acesso = True
        usuario.update = timezone.now()
        usuario.save()
        Alerta.set_mensagem("Usuário ativado com sucesso!")
        return redirect(
            "listar_usuarios",
        )

    @staticmethod
    @verificar_permissoes(codigo_model=1)
    def autenticar_usuario(email, senha):
        try:
            usuario = Usuario.objects.get(email__iexact=email)
            if check_password(senha, usuario.senha):
                return usuario
        except Usuario.DoesNotExist:
            pass
        return None

    @staticmethod
    @verificar_permissoes(codigo_model=1)
    def cadastrar_usuario(request):
        id_empresa = UserInfo.get_id_empresa(request)
        form_usuario = UsuarioForm()
        lojas = Loja.objects.filter(empresa_id=id_empresa)

        if request.method == "POST":
            form = UsuarioForm(request.POST)
            if form.is_valid():
                email_responsavel = form.cleaned_data["email"]
                if email_existe(email_responsavel):
                    Alerta.set_mensagem("O email já existe. Por favor, escolha outro.")
                    return view_usuarios.listar_usuarios(
                        request,
                        {
                            "form_usuario": form,
                            "list_lojas": lojas,
                            "open_modal": True,
                        },
                    )

                nome_usuario = (
                    form.cleaned_data["nome_completo"].replace(" ", "").lower()
                )
                while usuario_existe(nome_usuario):
                    nome_usuario = nome_usuario + gerar_numero_aleatorio()

                id_empresa = UserInfo.get_id_empresa(request)
                usuario = form.save(commit=False)
                usuario.empresa_id = id_empresa
                usuario.nome_usuario = nome_usuario
                usuario.senha = make_password(usuario.senha)
                usuario.save()
                for key, value in request.POST.items():
                    if key.startswith("status_acesso_"):
                        loja_id = key.replace("status_acesso_", "")
                        loja = get_object_or_404(Loja, id_loja=loja_id)
                        associacao = Associado.objects.create(
                            usuario=usuario, loja=loja
                        )
                        associacao.status_acesso = True if value == "on" else False
                        associacao.update = timezone.now()
                        associacao.save
                Alerta.set_mensagem("Usuário ativado com sucesso!")
                return redirect("configuracao_usuario", id_usuario=usuario.id_usuario)
            else:
                Alerta.set_mensagem("Formulário inválido. Por favor, corrija os erros.")
                return view_usuarios.listar_usuarios(
                    request,
                    {
                        "form_usuario": form_usuario,
                        "list_lojas": lojas,
                        "open_modal": True,
                    },
                )
        else:
            try:

                return view_usuarios.listar_usuarios(
                    request,
                    {
                        "form_usuario": form_usuario,
                        "list_lojas": lojas,
                        "open_modal": True,
                    },
                )
            except Loja.DoesNotExist:
                Alerta.set_mensagem(
                    "Para associar um usuario a loja, precisa criar uma!"
                )
                form_usuario = UsuarioForm()
                return view_usuarios.listar_usuarios(
                    request,
                    {
                        "form_usuario": form_usuario,
                        "open_modal": True,
                    },
                )

    @staticmethod
    @verificar_permissoes(codigo_model=1)
    def configuracao_usuario(request, id_usuario):
        if request.method == "POST":
            for key, value in request.POST.items():
                if key.startswith("status_acesso_"):
                    configuracao_id = key.replace("status_acesso_", "")
                    # Atualizar o status de acesso para a configuração correspondente
                    configuracao = Configuracao.objects.get(
                        id_configuracao=configuracao_id
                    )
                    configuracao.status_acesso = True if value == "on" else False
                    configuracao.update = timezone.now()
                    configuracao.save()
                    Alerta.set_mensagem("Configurações salvas com sucesso!")
            return redirect("listar_usuarios")
        else:
            list_configuracoes = Configuracao.objects.filter(usuario_id=id_usuario)

            # Verificar nao existem configurações para o usuário implementamos uma padrão
            if not list_configuracoes.exists():
                list_configuracoes = list_configuracoes_padrao(id_usuario, False)
                criar_configuracoes_padrao(list_configuracoes)
                list_configuracoes = Configuracao.objects.filter(usuario_id=id_usuario)

            return view_usuarios.listar_usuarios(
                request,
                {
                    "formularios_configuracao": list_configuracoes,
                    "open_modal_configuracao": True,
                },
            )
