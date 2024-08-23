from django.shortcuts import render, redirect, get_object_or_404
from api.user import UserInfo
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from ..models import Usuario, Configuracao, Loja, Associado
from .ConfiguracaoView import ConfiguracaoView
from api.utils import Utils
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from api.permissions import permissions,CustomPermission
from rest_framework.views import APIView
class UsuariosView(APIView):
    permission_classes = [CustomPermission(codigo_model="usuarios", auth_required=True)]


    @permissions.isAutorizado(1, True)
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
    def _atualizar_associados(request, usuario, list_lojas):
        try:
            # Carrega e decodifica os dados JSON do corpo da requisição
            data = json.loads(request.body)

            # Atualiza o status de acesso para cada loja
            for loja in list_lojas:
                campo_checkbox = f"status_acesso_{loja.id_loja}"
                status_acesso = campo_checkbox in data
                associacao, created = Associado.objects.get_or_create(
                    usuario_id=usuario.id_usuario,
                    loja_id=loja.id_loja,
                )
                associacao.status_acesso = status_acesso
                associacao.update = Utils.obter_data_hora_atual()
                associacao.save()

            return JsonResponse(
                {"message": "Associações atualizadas com sucesso!"}, status=200
            )

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    @staticmethod
    @require_http_methods(["GET"])
    @permissions.isAutorizado(1, True)
    def _editar_usuario_get(request, id_usuario):
        try:
            usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
            list_lojas = Loja.objects.filter(
                empresa_id=UserInfo.get_id_empresa(request)
            )
            associado = Associado.objects.filter(usuario=usuario)

            list_objs = []
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

            return JsonResponse(
                {
                    "form_usuario": {},
                    "list_lojas": list_objs,
                    "open_modal": True,
                    "isEditar": True,
                },
                status=200,
            )

        except Usuario.DoesNotExist:
            return JsonResponse({"message": "Usuário não encontrado."}, status=404)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    @staticmethod
    @require_http_methods(["POST"])
    @permissions.isAutorizado(1, True)
    def excluir_usuario(request):
        try:
            data = json.loads(request.body)
            id_usuario = data.get("id_usuario")

            if not id_usuario:
                return JsonResponse(
                    {"message": "ID do usuário não fornecido."}, status=400
                )

            usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
            usuario.delete()

            return JsonResponse(
                {"message": "Usuário excluído com sucesso!"}, status=200
            )

        except Usuario.DoesNotExist:
            return JsonResponse({"message": "Usuário não encontrado."}, status=404)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    @staticmethod
    @require_http_methods(["POST"])
    @permissions.isAutorizado(1, True)
    def bloquear_usuario(request):
        try:
            data = json.loads(request.body)
            id_usuario = data.get("id_usuario")

            if not id_usuario:
                return JsonResponse(
                    {"message": "ID do usuário não fornecido."}, status=400
                )

            usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
            usuario.status_acesso = False
            usuario.update = timezone.now()
            usuario.save()

            return JsonResponse(
                {"message": "Usuário bloqueado com sucesso!"}, status=200
            )

        except Usuario.DoesNotExist:
            return JsonResponse({"message": "Usuário não encontrado."}, status=404)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    @staticmethod
    @require_http_methods(["POST"])
    @permissions.isAutorizado(1, True)
    def ativar_usuario(request):
        try:
            data = json.loads(request.body)
            id_usuario = data.get("id_usuario")

            if not id_usuario:
                return JsonResponse(
                    {"message": "ID do usuário não fornecido."}, status=400
                )

            usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
            usuario.status_acesso = True
            usuario.update = timezone.now()
            usuario.save()

            return JsonResponse({"message": "Usuário ativado com sucesso!"}, status=200)

        except Usuario.DoesNotExist:
            return JsonResponse({"message": "Usuário não encontrado."}, status=404)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    @staticmethod
    @permissions.isAutorizado(1, True)
    def autenticar_usuario(email, senha):
        try:
            usuario = Usuario.objects.get(email__iexact=email)
            if check_password(senha, usuario.senha):
                return usuario
        except Usuario.DoesNotExist:
            pass
        return None

    @staticmethod
    @require_http_methods(["POST"])
    @permissions.isAutorizado(1, True)
    def cadastrar_usuario(request):
        try:
            # Obtém o ID da empresa do usuário autenticado
            id_empresa = UserInfo.get_id_empresa(request)
            lojas = Loja.objects.filter(empresa_id=id_empresa)

            # Carrega e decodifica os dados JSON do corpo da requisição
            data = json.loads(request.body)

            # Extrai os dados do JSON
            nome_completo = data.get("nome_completo")
            email_responsavel = data.get("email_responsavel")
            senha = data.get("senha")
            status_acesso = data.get("status_acesso", {})

            if not nome_completo or not email_responsavel or not senha:
                return JsonResponse(
                    {"message": "Campos obrigatórios faltando."}, status=400
                )

            # Verifica se o email já está cadastrado
            if Utils.email_existe(email_responsavel):
                return JsonResponse(
                    {
                        "message": "O email já está cadastrado em nossa base de dados, escolha outro."
                    },
                    status=400,
                )

            # Gera um nome de usuário único
            nome_usuario = nome_completo.replace(" ", "").lower()
            while Utils.usuario_existe(nome_usuario):
                nome_usuario += Utils.gerar_numero_aleatorio()

            # Cria e salva o usuário
            usuario = Usuario(
                nome_completo=nome_completo,
                email=email_responsavel,
                senha=make_password(senha),
                empresa_id=id_empresa,
                nome_usuario=nome_usuario,
                status_acesso=True,
            )
            usuario.save()

            # Associa o usuário às lojas conforme o status de acesso
            for loja_id, acesso in status_acesso.items():
                loja = get_object_or_404(Loja, id_loja=loja_id)
                Associado.objects.create(
                    usuario=usuario,
                    loja=loja,
                    status_acesso=acesso == "on",
                )

            return JsonResponse({"message": "Usuário ativado com sucesso!"}, status=201)

        except Loja.DoesNotExist:
            return JsonResponse(
                {
                    "message": "Para associar um usuário a uma loja, é necessário criar uma loja."
                },
                status=404,
            )

        except Exception as e:
            # Captura e retorna qualquer outro erro inesperado
            return JsonResponse({"message": str(e)}, status=500)

    @staticmethod
    @require_http_methods(["POST"])
    @permissions.isAutorizado(1, True)
    def configuracao_usuario(request, id_usuario):
        try:
            # Carrega e decodifica os dados JSON do corpo da requisição
            data = json.loads(request.body)

            # Verifica se os dados contêm configurações
            if "configuracoes" in data:
                for key, value in data["configuracoes"].items():
                    if key.startswith("status_acesso_"):
                        configuracao_id = key.replace("status_acesso_", "")
                        # Atualiza o status de acesso para a configuração correspondente
                        configuracao = get_object_or_404(
                            Configuracao, id_configuracao=configuracao_id
                        )
                        configuracao.status_acesso = value == "on"
                        configuracao.update = timezone.now()
                        configuracao.save()

                return JsonResponse(
                    {"message": "Configurações salvas com sucesso!"}, status=200
                )
            else:
                return JsonResponse(
                    {
                        "message": "Dados de configuração não encontrados no corpo da requisição."
                    },
                    status=400,
                )

        except Configuracao.DoesNotExist:
            return JsonResponse({"message": "Configuração não encontrada."}, status=404)

        except Exception as e:
            # Captura e retorna qualquer outro erro inesperado
            return JsonResponse({"message": str(e)}, status=500)

    def email_existe(email):
        from api.models import Usuario

        return Usuario.objects.filter(email__iexact=email).exists()

    def usuario_existe(usuario):
        from api.models import Usuario

        return Usuario.objects.filter(nome_usuario__iexact=usuario).exists()
