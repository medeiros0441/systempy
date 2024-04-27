from django.shortcuts import render, get_object_or_404, redirect
from ..forms import LojaForm, EnderecoForm
from ..utils import utils
from ..static import Alerta, UserInfo
from ..models import Empresa, Loja, Associado, Usuario


class views_loja:
    @utils.verificar_permissoes(5)
    def lista_lojas(request, context=None):
        id_empresa = UserInfo.get_id_empresa(request, True)

        if context is None:
            context = {}

        try:
            lojas = Loja.objects.filter(empresa=id_empresa)

            context["lojas"] = lojas
        except Loja.DoesNotExist:
            # Caso a loja não exista, simplesmente não adicionamos nada ao contexto.
            pass
        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = utils.criar_alerta_js(alerta)
        return render(request, "loja/lista_lojas.html", context)
   
    @utils.verificar_permissoes(5)
    def criar_loja(request):
        try:
            if request.method == "POST":
                form_loja = LojaForm(request.POST)
                form_endereco = EnderecoForm(request.POST)

                id_empresa_get = UserInfo.get_id_empresa(request, True)
                # Obtenha a instância da Empresa com base no ID
                empresa_instance = get_object_or_404(Empresa, id_empresa=id_empresa_get)
                # Verifique se a instância da Empresa foi encontrada
                if empresa_instance:
                    form_loja.instance.empresa = empresa_instance

                if form_endereco.is_valid() and form_loja.is_valid():
                    endereco = form_endereco.save()  # Cria um novo registro de Endereco
                    form_loja.instance.endereco = endereco  # Associa o endereço à loja
                    loja = form_loja.save()  # Cria um novo registro de Loja
                    Alerta.set_mensagem("Cadastrado com Sucesso.")

                    id_usuario = UserInfo.get_id_usuario(request)
                    usuario = Usuario.objects.get(id_usuario=id_usuario)
                    associacao = Associado.objects.create(
                        usuario_id=id_usuario, loja=loja
                    )
                    if usuario.nivel_usuario == 1:
                        associacao.status_acesso = True
                    else:
                        associacao.status_acesso = False
                    associacao.save

                    Alerta.set_mensagem(f"Loja {loja.nome_loja} criada com sucesso")
                    return redirect("lista_lojas")
                else:
                    if not form_endereco.is_valid():
                        Alerta.set_mensagem("Formulário de Endereço inválido.")
                    elif not form_loja.is_valid():
                        Alerta.set_mensagem("Formulário de Loja inválido.")
                    # Renderiza o template com os formulários inválidos
                    return views_loja.views_loja.lista_lojas(
                        request,
                        {
                            "open_modal": True,
                            "form_endereco": form_endereco,
                            "form_loja": form_loja,
                        },
                    )
            else:
                formloja = LojaForm()
                form = EnderecoForm()
                return views_loja.lista_lojas(
                    request,
                    {"open_modal": True, "form_endereco": form, "form_loja": formloja},
                )
        except Exception as e:
            mensagem_erro = str(e)
            return utils.erro(request, mensagem_erro)

    @utils.verificar_permissoes(5)
    def selecionar_loja(request, id_loja):

        try:
            loja = get_object_or_404(Loja, pk=id_loja)
            id = UserInfo.get_id_empresa(request)
            if loja.empresa.id_empresa == id:
                return views_loja.lista_lojas(
                    request,
                    {
                        "open_modal": True,
                        "text_endereco": loja.endereco,
                        "text_loja": loja,
                    },
                )
            else:
                return utils.erro(request, "vôce não está associado a empresa..")
        except Exception as e:
            mensagem_erro = str(e)
            return utils.erro(request, mensagem_erro)

    @utils.verificar_permissoes(5)
    def editar_loja(request, id_loja):
        loja = get_object_or_404(Loja, pk=id_loja)
        id = UserInfo.get_id_empresa(request)
        if loja.empresa.id_empresa != id:
            return utils.erro(request, "vôce não está associado a empresa..")
        if request.method == "POST":
            form_loja = LojaForm(request.POST, instance=loja)
            form_endereco = EnderecoForm(request.POST, instance=loja.endereco)

            if form_endereco.is_valid() and form_loja.is_valid():
                endereco = form_endereco.save()  # Cria um novo registro de Endereco
                form_loja.instance.endereco = endereco  # Associa o endereço à loja
                form_loja.save()  # Cria um novo registro de Loja
                Alerta.set_mensagem("Cadastrado com Sucesso.")
                return redirect("lista_lojas")
            else:
                if not form_endereco.is_valid():
                    Alerta.set_mensagem("Formulário de Endereço inválido.")
                elif not form_loja.is_valid():
                    Alerta.set_mensagem("Formulário de Loja inválido.")
                # Renderiza o template com os formulários inválidos
                return views_loja.lista_lojas(
                    request,
                    {
                        "open_modal": True,
                        "form_endereco": form_endereco,
                        "form_loja": form_loja,
                    },
                )

        else:
            formloja = LojaForm(instance=loja)
            form = EnderecoForm(instance=loja.endereco)
            return views_loja.lista_lojas(
                request,
                {"open_modal": True, "form_endereco": form, "form_loja": formloja},
            )

    @utils.verificar_permissoes(5)
    def excluir_loja(request, id_loja):
        loja = get_object_or_404(Loja, id_loja=id_loja)
        loja.delete()
        Alerta.set_mensagem("Loja excluído com sucesso.")
        return redirect("lista_lojas")
