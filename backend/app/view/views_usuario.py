from django.shortcuts import render, redirect, get_object_or_404
from app.static import Alerta, UserInfo
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from ..models import Usuario, Configuracao, Loja, Associado
from .views_configuracao import views_configuracao
from app.utils import Utils
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder


class views_usuarios:

    @staticmethod
    @Utils.verificar_permissoes(1, True)
    def listar_usuarios(request, context=None):
        id_empresa = UserInfo.get_id_empresa(request)

        usuarios = Usuario.objects.filter(empresa=id_empresa)
        if context is None:
            context = {}
        context["usuarios"] = usuarios
        alerta_js = Alerta.get_mensagem()
        if alerta_js:
            context["alerta_js"] = Utils.criar_alerta_js(alerta_js)

        return render(request, "usuario/lista_usuario.html", context)

    @Utils.verificar_permissoes(1, True)
    def api_listar_usuarios(request):
        try:
            id_empresa = UserInfo.get_id_empresa(request)
            usuarios = Usuario.objects.filter(empresa_id=id_empresa)
            usuarios_json = [
                {
                    "id_usuario": usuario.id_usuario,
                    "nome_completo": usuario.nome_completo,
                    "nome_usuario": usuario.nome_usuario,
                    "email": usuario.email,
                    "ultimo_login": (
                        usuario.ultimo_login.strftime("%Y-%m-%d %H:%M:%S")
                        if usuario.ultimo_login
                        else None
                    ),
                    "nivel_usuario": usuario.nivel_usuario,
                    "status_acesso": usuario.status_acesso,
                    "insert": usuario.insert,
                    "update": usuario.update,
                    "empresa": usuario.empresa.id_empresa,
                }
                for usuario in usuarios
            ]
            return JsonResponse({"usuarios": usuarios_json, "success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @Utils.verificar_permissoes(1, True)
    def detalhes_usuario(request, id_usuario):
        usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        associados = Associado.objects.filter(usuario=usuario)

        associados_list = []
        for associado in associados:
            status = "Autorizado" if associado.status_acesso else "Não Permitido"
            associados_list.append(
                {
                    "status": status,
                    "nome": associado.loja.nome,
                    "atualizado": associado.update,
                }
            )

        return views_usuarios.listar_usuarios(
            request,
            {
                "open_modal": True,
                "text_usuario": usuario,
                "associados_list": associados_list,
            },
        )

    @staticmethod
    @Utils.verificar_permissoes(1, True)
    def editar_usuario(request, id_usuario):
        try:
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            id_empresa = UserInfo.get_id_empresa(request)
            list_lojas = Loja.objects.filter(empresa_id=id_empresa)

            if request.method == "POST":
                usuario = views_usuarios._editar_usuario_post(
                    request, usuario, list_lojas
                )
                return redirect("listar_usuarios")
            else:
                return views_usuarios._editar_usuario_get(request, usuario, list_lojas)

        except (Associado.DoesNotExist, Loja.DoesNotExist):
            pass
        Alerta.set_mensagem("Para associar um usuário à loja, precisa criar uma!")
        form_usuario = {}
        return views_usuarios.listar_usuarios(
            request,
            {
                "form_usuario": form_usuario,
                "open_modal": True,
                "isEditar": True,
            },
        )

    def _editar_usuario_post(request, usuario, list_lojas):
        usuario.nome_completo = request.POST.get("nome_completo", usuario.nome_completo)
        if usuario.nivel_usuario > 1:
            usuario.nivel_usuario = request.POST.get(
                "nivel_usuario", usuario.nivel_usuario
            )
            usuario.status_acesso = request.POST.get(
                "status_acesso", usuario.status_acesso
            )

        if usuario.nome_completo:
            usuario.update = Utils.obter_data_hora_atual()
            usuario.save()
            views_usuarios._atualizar_associados(request, usuario, list_lojas)
            Alerta.set_mensagem("Usuário editado com sucesso!")
        else:
            Alerta.set_mensagem("Formulário inválido. Por favor, corrija os erros.")

    def _atualizar_associados(request, usuario, list_lojas):
        for loja in list_lojas:
            campo_checkbox = f"status_acesso_{loja.id_loja}"
            associacao, created = Associado.objects.get_or_create(
                usuario_id=usuario.id_usuario,
                loja_id=loja.id_loja,
            )
            associacao.status_acesso = campo_checkbox in request.POST
            associacao.update = Utils.obter_data_hora_atual()
            associacao.save()

    def _editar_usuario_get(request, usuario, list_lojas):
        form_usuario = { }
        list_objs = []

        associado = Associado.objects.filter(usuario=usuario)

        for loja in list_lojas:
            loja_info = {
                "id_loja": loja.id_loja,
                "nome": loja.nome,
                "status_acesso": False,
            }
            associado_loja = associado.filter(
                loja_id=loja.id_loja, usuario=usuario
            ).first()
            if associado_loja:
                loja_info["status_acesso"] = associado_loja.status_acesso

            list_objs.append(loja_info)

        return views_usuarios.listar_usuarios(
            request,
            {
                "form_usuario": form_usuario,
                "list_lojas": list_objs,
                "open_modal": True,
                "isEditar": True,
            },
        )

    @staticmethod
    @Utils.verificar_permissoes(1, True)
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
    @Utils.verificar_permissoes(1, True)
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
    @Utils.verificar_permissoes(1, True)
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
    @Utils.verificar_permissoes(1, True)
    def autenticar_usuario(email, senha):
        try:
            usuario = Usuario.objects.get(email__iexact=email)
            if check_password(senha, usuario.senha):
                return usuario
        except Usuario.DoesNotExist:
            pass
        return None

    @staticmethod
    @Utils.verificar_permissoes(1, True)
    def cadastrar_usuario(request):
        id_empresa = UserInfo.get_id_empresa(request)
        form_usuario = {}
        lojas = Loja.objects.filter(empresa_id=id_empresa)

        if request.method == "POST":
            form =   {}
            if form.is_valid():
                email_responsavel = form.cleaned_data["email"]
                email_responsavel.lower().strip()
                if Utils.email_existe(email_responsavel):
                    Alerta.set_mensagem(
                        "O email já está cadastrado em nossa base de dados, escolha outro."
                    )
                    return views_usuarios.listar_usuarios(
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
                while Utils.usuario_existe(nome_usuario):
                    nome_usuario = nome_usuario + Utils.gerar_numero_aleatorio()

                id_empresa = UserInfo.get_id_empresa(request)
                usuario = form.save(commit=False)
                usuario.email = email_responsavel
                usuario.empresa_id = id_empresa
                usuario.status_acesso = True
                usuario.nome_usuario = nome_usuario
                usuario.senha = make_password(usuario.senha)
                usuario.save()
                for key, value in request.POST.items():
                    if key.startswith("status_acesso_"):
                        loja_id = key.replace("status_acesso_", "")
                        loja = get_object_or_404(Loja, id_loja=loja_id)
                        Associado.objects.create(
                            usuario=usuario,
                            loja=loja,
                            status_acesso=True if value == "on" else False,
                        )
                Alerta.set_mensagem("Usuário ativado com sucesso!")
                return redirect("configuracao_usuario", id_usuario=usuario.id_usuario)
            else:
                Alerta.set_mensagem("Formulário inválido. Por favor, corrija os erros.")
                return views_usuarios.listar_usuarios(
                    request,
                    {
                        "form_usuario": form_usuario,
                        "list_lojas": lojas,
                        "open_modal": True,
                    },
                )
        else:
            try:

                return views_usuarios.listar_usuarios(
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
                form_usuario = {}
                return views_usuarios.listar_usuarios(
                    request,
                    {
                        "form_usuario": form_usuario,
                        "open_modal": True,
                    },
                )

    @staticmethod
    @Utils.verificar_permissoes(1, True)
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
                list_configuracoes = views_configuracao.list_configuracoes_padrao(
                    id_usuario, False
                )
                views_configuracao.criar_configuracoes_padrao(list_configuracoes)
                list_configuracoes = Configuracao.objects.filter(usuario_id=id_usuario)

            return views_usuarios.listar_usuarios(
                request,
                {
                    "formularios_configuracao": list_configuracoes,
                    "open_modal_configuracao": True,
                },
            )
