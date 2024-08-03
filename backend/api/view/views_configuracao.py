from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from ..models import Configuracao, Usuario
from django.urls import reverse_lazy
from api.utils import Utils
from api.permissions import permissions, CustomPermission
from rest_framework.views import APIView


class views_configuracao(APIView):
    permission_classes = [
        CustomPermission(codigo_model="configuracao", auth_required=True)
    ]

    def get_configuracoes_usuario(id_usuario):
        try:

            configuracoes_usuario = Configuracao.objects.filter(usuario_id=id_usuario)
            return configuracoes_usuario
        except Usuario.DoesNotExist:
            return None
        except Configuracao.DoesNotExist:
            return None

    def configuracao_set_session(request, id_usuario):
        try:
            configuracoes_usuario = Configuracao.objects.filter(usuario_id=id_usuario)
            if configuracoes_usuario:
                configuracoes_serializadas = {
                    config["codigo"]: config["status_acesso"]
                    for config in configuracoes_usuario.values()
                    if config["status_acesso"]
                }
                request.session["configs_ativos"] = configuracoes_serializadas
                return True
            else:
                return False
        except Exception as e:
            print(f"Erro ao definir configurações na sessão: {str(e)}")
            return False

    def criar_configuracoes_padrao(listModel):
        for model in listModel:
            Configuracao.objects.create(
                titulo=model.titulo,
                descricao_interna=model.descricao_interna,
                descricao=model.descricao,
                status_acesso=model.status_acesso,
                codigo=model.codigo,
                usuario=model.usuario,
            )

    def list_configuracoes_padrao(usuario=None, status=True):

        classes = Utils.lista_de_configuracao()

        list_configuracao = []

        for classe in classes:
            nome_classe = classe["nome"]
            codigo_interger = classe["codigo"]
            titulo = f"Gerenciamento de {nome_classe}"
            descricao_interna = (
                f"Controle de {nome_classe.lower()}, editar, alterar, criar..."
            )
            descricao = f"Permitir acesso ao Painel de {nome_classe}, isso inclui criar, editar, remover, entre outros."
            status_acesso = status
            id = usuario.id_usuario if hasattr(usuario, "id_usuario") else usuario

            configuracao = Configuracao(
                titulo=titulo,
                descricao_interna=descricao_interna,
                descricao=descricao,
                status_acesso=status_acesso,
                codigo=codigo_interger,
                usuario_id=id,
            )
            list_configuracao.append(configuracao)

        return list_configuracao
