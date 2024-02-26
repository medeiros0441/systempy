from django.shortcuts import render, get_object_or_404, redirect
from ..models.endereco import Endereco
from ..forms.EnderecoForm import EnderecoForm


def lista_endereco(request):
    enderecos = Endereco.objects.all()
    return render(request, "endereco/lista_endereco.html", {"enderecos": enderecos})


def criar_endereco(request):
    if request.method == "POST":
        form = EnderecoForm(request.POST)
        if form.is_valid():
            form.save()
            # Faça o que precisar após salvar o endereço
    else:
        form = EnderecoForm()
    return render(request, "endereco/criar_endereco.html", {"form": form})


def selecionar_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    return render(request, "endereco/selecionar_endereco.html", {"endereco": endereco})


def editar_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    if request.method == "POST":
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            return redirect("lista_endereco")
    else:
        form = EnderecoForm(instance=endereco)
    return render(request, "endereco/editar_endereco.html", {"form": form})


def delete_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    if request.method == "POST":
        endereco.delete()
        return redirect("lista_endereco")
    return render(request, "endereco/delete_endereco.html", {"endereco": endereco})
