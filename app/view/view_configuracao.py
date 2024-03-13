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


def criar_configuracoes_padrao(usuario):

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

    for nome_classe in nomes_classes:
        titulo = f"Gerenciamento de {nome_classe}"
        descricao_interna = (
            f"Controle de {nome_classe.lower()}, editar, alterar, criar..."
        )
        descricao = f"Permitir acesso ao Painel de {nome_classe}, isso inclui criar, editar, remover, entre outros."
        status_acesso = True
        Configuracao.objects.create(
            titulo=titulo,
            descricao=descricao,
            descricao_interna=descricao_interna,
            status_acesso=status_acesso,
            usuario=usuario,
        )
