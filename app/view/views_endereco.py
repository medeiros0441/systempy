from django.shortcuts import render, get_object_or_404, redirect
from ..models import Endereco, Configuracao
from ..forms import EnderecoForm
from app.utils import Utils
from app.static import Alerta, UserInfo
from django.db import IntegrityError


class views_endereco:

    @staticmethod
    @Utils.verificar_permissoes(codigo_model=3)
    def lista_enderecos(request, context=None):
        if context is None:
            context = {}

        enderecos = Endereco.objects.all()
        context["enderecos"] = enderecos
        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = Utils.criar_alerta_js(alerta)

        return render(request, "endereco/lista_enderecos.html", context)

    @staticmethod
    @Utils.verificar_permissoes(codigo_model=3)
    def criar_endereco(request):
        if request.method == "POST":
            form = EnderecoForm(request.POST)
            if form.is_valid():
                form.save()
                Alerta.set_mensagem("Cadastrado com Sucesso.")
                return redirect("lista_enderecos")

            else:
                return views_endereco.lista_enderecos(
                    request, {"open_modal": True, "form": form}
                )
        else:
            form = EnderecoForm()
            return views_endereco.lista_enderecos(
                request, {"open_modal": True, "form": form}
            )

    @staticmethod
    @Utils.verificar_permissoes(codigo_model=3)
    def selecionar_endereco(request, pk):
        endereco = get_object_or_404(Endereco, pk=pk)
        return views_endereco.lista_enderecos(
            request, {"open_modal": True, "endereco": endereco}
        )

    @staticmethod
    @Utils.verificar_permissoes(codigo_model=3)
    def editar_endereco(request, pk):
        endereco = get_object_or_404(Endereco, pk=pk)
        if request.method == "POST":
            form = EnderecoForm(request.POST, instance=endereco)
            if form.is_valid():
                form.save()
                Alerta.set_mensagem("Endereço Editado")
                return redirect("lista_enderecos")

        else:
            form = EnderecoForm(instance=endereco)
            return views_endereco.lista_enderecos(
                request, {"open_modal": True, "form": form}
            )

    @staticmethod
    @Utils.verificar_permissoes(codigo_model=3)
    def delete_endereco(request, pk):
        try:
            endereco = get_object_or_404(Endereco, pk=pk)
            endereco.delete()
            Alerta.set_mensagem("Endereço excluído com sucesso.")
        except IntegrityError as e:
            # Captura o erro de integridade e fornece uma mensagem adequada
            Alerta.set_mensagem(
                "Não é possível excluir este endereço. Está sendo usado em outro lugar."
            )
        return redirect("lista_enderecos")
