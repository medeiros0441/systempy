from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from ..models import Configuracao
from django.urls import reverse_lazy


class ConfiguracaoListView(ListView):
    model = Configuracao
    template_name = "configuracao/list_configuracao.html"
    context_object_name = "configuracoes"


class ConfiguracaoDetailView(DetailView):
    model = Configuracao
    template_name = "configuracao/configuracao_detail.html"
    context_object_name = "configuracao"


class ConfiguracaoCreateView(CreateView):
    model = Configuracao
    template_name = "configuracao/configuracao_form.html"
    fields = ["usuario", "titulo", "descricao", "descricao_intera", "status"]
    success_url = reverse_lazy("configuracao_list")


class ConfiguracaoUpdateView(UpdateView):
    model = Configuracao
    template_name = "configuracao/configuracao_form.html"
    fields = ["usuario", "titulo", "descricao", "descricao_interna", "status"]
    success_url = reverse_lazy("configuracao_list")


class ConfiguracaoDeleteView(DeleteView):
    model = Configuracao
    template_name = "configuracao/configuracao_confirm_delete.html"
    success_url = reverse_lazy("configuracao_list")


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

    classes = [
        {"nome": "Usuario", "codigo": 1},
        {"nome": "Empresa", "codigo": 2},
        {"nome": "Endereco", "codigo": 3},
        {"nome": "Galao", "codigo": 4},
        {"nome": "Loja", "codigo": 5},
        {"nome": "Produto", "codigo": 6},
        {"nome": "Venda", "codigo": 7},
        {"nome": "Cliente", "codigo": 8},
        {"nome": "Motoboy", "codigo": 9},
    ]

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
            usuario_id=usuario,
        )
        list_configuracao.append(configuracao)

    return list_configuracao
