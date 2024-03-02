from django.shortcuts import render, get_object_or_404, redirect
from ..models.endereco import Endereco
from ..forms.EnderecoForm import EnderecoForm
from ..def_global import criar_alerta_js
from ..static import Alerta


def lista_endereco(request, context=None):
    if context is None:
        context = {}

    enderecos = Endereco.objects.all()
    context["enderecos"] = enderecos
    alerta = Alerta.get_mensagem()
    if alerta:
        context["alerta_js"] = criar_alerta_js(alerta)

    return render(request, "endereco/lista_endereco.html", context)


def criar_endereco(request):
    if request.method == "POST":
        form = EnderecoForm(request.POST)
        if form.is_valid():
            form.save()
            Alerta.set_mensagem("Cadastrado com Sucesso.")
            return redirect("lista_endereco")

        else:
            return lista_endereco(request, {"open_modal": True, "form": form})
    else:
        form = EnderecoForm()
        return lista_endereco(request, {"open_modal": True, "form": form})


def selecionar_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    return lista_endereco(request, {"open_modal": True, "endereco": endereco})


def editar_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    if request.method == "POST":
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            Alerta.set_mensagem("Endereço Editado")
            return redirect("lista_endereco")

    else:
        form = EnderecoForm(instance=endereco)
        return lista_endereco(request, {"open_modal": True, "form": form})


def delete_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    endereco.delete()
    Alerta.set_mensagem("Endereço excluído com sucesso.")
    return redirect("lista_endereco")
