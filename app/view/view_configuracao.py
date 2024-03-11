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
    fields = ["usuario", "titulo", "descricao", "descricao_intera", "status"]
    success_url = reverse_lazy("configuracao_list")


class ConfiguracaoDeleteView(DeleteView):
    model = Configuracao
    template_name = "configuracao/configuracao_confirm_delete.html"
    success_url = reverse_lazy("configuracao_list")
