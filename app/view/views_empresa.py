# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from ..models.empresa import Empresa


def listar_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, "cliente/empresa/lista_empresa.html", {"empresas": empresas})


def criar_empresa(request):
    if request.method == "POST":
        nome_empresa = request.POST.get("nome_empresa")
        nro_cnpj = request.POST.get("nro_cnpj")
        razao_social_empresa = request.POST.get("razao_social_empresa", "")
        descricao_empresa = request.POST.get("descricao_empresa", "")
        nome_responsavel = request.POST.get("nome_responsavel")
        cargo_responsavel = request.POST.get("cargo_responsavel")
        email_responsavel = request.POST.get("email_responsavel")
        telefone_responsavel = request.POST.get("telefone_responsavel")

        Empresa.objects.create(
            nome_empresa=nome_empresa,
            nro_cnpj=nro_cnpj,
            razao_social_empresa=razao_social_empresa,
            descricao_empresa=descricao_empresa,
            nome_responsavel=nome_responsavel,
            cargo_responsavel=cargo_responsavel,
            email_responsavel=email_responsavel,
            telefone_responsavel=telefone_responsavel,
        )
        return redirect("empresa/listar_empresa")
    return render(request, "default/cadastro.html")


def detalhes_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    return render(request, "detalhes_empresa.html", {"empresa": empresa})


def editar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == "POST":
        empresa.nome_empresa = request.POST.get("nome_empresa")
        empresa.nro_cnpj = request.POST.get("nro_cnpj")
        empresa.razao_social_empresa = request.POST.get("razao_social_empresa", "")
        empresa.descricao_empresa = request.POST.get("descricao_empresa", "")
        empresa.nome_responsavel = request.POST.get("nome_responsavel")
        empresa.cargo_responsavel = request.POST.get("cargo_responsavel")
        empresa.email_responsavel = request.POST.get("email_responsavel")
        empresa.telefone_responsavel = request.POST.get("telefone_responsavel")
        empresa.save()
        return redirect("detalhes_empresa", pk=pk)
    return render(request, "editar_empresa.html", {"empresa": empresa})


def excluir_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == "POST":
        empresa.delete()
        return redirect("listar_empresas")
    return render(request, "confirmar_exclusao_empresa.html", {"empresa": empresa})
