from django import forms
from ..models import Venda,Loja,Cliente
from ..static import UserInfo


class VendaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)

        # Definindo as opções para o campo loja
        id_empresa = UserInfo.get_id_empresa(
            kwargs.get("request")
        )  # Supondo que você tenha um método como get_id_empresa em UserInfo
        lojas = Loja.objects.filter(empresa=id_empresa)
        choices_loja = [("", "Selecione uma loja")] + [
            (str(loja.id_loja), loja.nome_loja) for loja in lojas
        ]
        self.fields["loja"].widget.choices = choices_loja

        # Definindo as opções para o campo cliente
        clientes = (
            Cliente.objects.all()
        )  # Ou você pode filtrar os clientes de acordo com a lógica do seu aplicativo
        choices_cliente = [("", "Selecione um cliente")] + [
            (str(cliente.id), cliente.nome) for cliente in clientes
        ]
        self.fields["cliente"].widget.choices = choices_cliente

    class Meta:
        model = Venda
        fields = [
            "data_venda",
            "valor_total",
            "forma_pagamento",
            "tipo_venda",
            "descricao",
            "usuario",
            "loja",
            "cliente",
        ]
        widgets = {
            "data_venda": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "valor_total": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "forma_pagamento": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_venda": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control"}),
            "usuario": forms.Select(attrs={"class": "form-control"}),
            "loja": forms.Select(attrs={"class": "form-control"}),
            "cliente": forms.Select(attrs={"class": "form-control"}),
        }
