from django.shortcuts import render, get_object_or_404, redirect
from ..models.loja import Loja
from ..forms.LojaForm import LojaForm
from ..forms.EnderecoForm import EnderecoForm
from ..def_global import criar_alerta_js, erro
from ..static import Alerta, UserInfo


def lista_loja(request, context=None):
    id_empresa = UserInfo.get_id_empresa(request)
    id_usuario = UserInfo.get_id_usuario(request)

    if id_empresa != 0 and id_usuario != 0:
        if context is None:
            context = {}

        try:
            lojas = Loja.objects.get(empresa=id_empresa)
            context["lojas"] = lojas
        except Loja.DoesNotExist:
            # Caso a loja não exista, simplesmente não adicionamos nada ao contexto.
            pass

        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = criar_alerta_js(alerta)

        return render(request, "loja/lista_loja.html", context)
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def criar_loja(request):
    if request.method == "POST":
        form = LojaForm(request.POST)
        if form.is_valid():
            form.save()
            Alerta.set_mensagem("Cadastrado com Sucesso.")
            return redirect("lista_loja")

        else:
            return lista_loja(request, {"open_modal": True, "form": form})
    else:
        formloja = LojaForm()
        form = EnderecoForm()
        return lista_loja(
            request, {"open_modal": True, "form_endereco": form, "form_loja": formloja}
        )


def selecionar_loja(request, pk):
    loja = get_object_or_404(Loja, pk=pk)
    return lista_loja(request, {"open_modal": True, "loja": loja})


def editar_loja(request, pk):
    loja = get_object_or_404(Loja, pk=pk)
    if request.method == "POST":
        form = LojaForm(request.POST, instance=loja)
        if form.is_valid():
            form.save()
            Alerta.set_mensagem("Loja Editado")
            return redirect("lista_loja")

    else:
        form = LojaForm(instance=loja)
        return lista_loja(request, {"open_modal": True, "form": form})


def delete_loja(request, pk):
    loja = get_object_or_404(Loja, pk=pk)
    loja.delete()
    Alerta.set_mensagem("Loja excluído com sucesso.")
    return redirect("lista_loja")
