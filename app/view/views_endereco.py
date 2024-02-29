from django.shortcuts import render, get_object_or_404, redirect
from ..models.endereco import Endereco
from ..forms.EnderecoForm import EnderecoForm

from ..def_global import criar_alerta_js


def lista_endereco(request, alerta_js=None):
    enderecos = Endereco.objects.all()
    context = {
        "enderecos": enderecos,
    }
    if alerta_js:
        context["alerta_js"] = criar_alerta_js(alerta_js)

    return render(request, "endereco/lista_endereco.html", context)


def criar_endereco(request):
    if request.method == "POST":
        form = EnderecoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "lista_endereco_alerta", alerta_js="Cadastrado com Sucesso."
            )
        else:
            erro = form.errors
            return render(
                request,
                "endereco/lista_endereco.html",
                {"open_modal": True, "form": form, "alerta_js": criar_alerta_js(erro)},
            )
    else:
        form = EnderecoForm()
    return render(
        request, "endereco/lista_endereco.html", {"open_modal": True, "form": form}
    )


def selecionar_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    return render(
        request, "endereco/lista_endereco.html", {"open_modal": True, "form": endereco}
    )


def editar_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    if request.method == "POST":
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            return redirect(
                "lista_endereco_alerta", alerta_js="erro, Ao excluir endereço"
            )
    else:
        form = EnderecoForm(instance=endereco)
    return render(
        request, "endereco/lista_endereco.html", {"open_modal": True, "form": form}
    )


def delete_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    if request.method == "POST":
        endereco.delete()
        return redirect("lista_endereco_alerta")
    return redirect("lista_endereco_alerta", alerta_js="erro, Ao excluir endereço")
