from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from ..models import Configuracao
from django.urls import reverse_lazy
from ..utils import utils


class views_configuracao:
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

        classes = utils.lista_de_configuracao()

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
            configuracao = Configuracao(
                titulo=titulo,
                descricao_interna=descricao_interna,
                descricao=descricao,
                status_acesso=status_acesso,
                codigo=codigo_interger,
                usuario_id=usuario.id_usuario,
            )
            list_configuracao.append(configuracao)

        return list_configuracao
