from django import forms
from ..models import Produto,Loja
from ..static import UserInfo
from decimal import Decimal


class ProdutoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ProdutoForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            existing_classes = self.fields[field_name].widget.attrs.get("class", "")
            self.fields[field_name].widget.attrs["class"] = (
                existing_classes + " form-control form-control-validate input"
            )

        self.fields["loja"].widget.attrs["class"] = "form-select form-select-sm"

        # Adicionando campos fake para exibição formatada
        self.fields["preco_compra_fake"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "form-control form-control-validate input money-mask",
                }
            ),
        )
        self.fields["preco_venda_fake"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "form-control form-control-validate input money-mask",
                }
            ),
        )
        instance = kwargs.get("instance")
        if instance:
            self.fields["preco_compra_fake"].initial = instance.preco_compra
            self.fields["preco_venda_fake"].initial = instance.preco_venda
        id_empresa = UserInfo.get_id_empresa(request)
        lojas = Loja.objects.filter(empresa=id_empresa)
        if request:
            choices = [("", "Selecione uma loja")]  # Primeiro item, vazio por padrão
            choices += [
                (str(loja.id_loja), loja.nome_loja) for loja in lojas
            ]  # Adiciona outras lojas
            self.fields["loja"].widget.choices = choices

    class Meta:
        model = Produto
        fields = [
            "nome",
            "quantidade_atual_estoque",
            "quantidade_minima_estoque",
            "preco_compra",
            "preco_venda",
            "fabricante",
            "loja",
        ]

    def clean(self):
        cleaned_data = super().clean()
        preco_compra_fake = cleaned_data.get("preco_compra_fake")
        preco_venda_fake = cleaned_data.get("preco_venda_fake")

        if preco_compra_fake:
            # Remover vírgulas e pontos da string
            preco_compra2 = preco_compra_fake.replace(",", ".")
            # Converter para Decimal
            preco_compra = Decimal(preco_compra2)
            cleaned_data["preco_compra"] = preco_compra

        if preco_venda_fake:
            preco_venda2 = preco_venda_fake.replace(",", ".")
            preco_venda = Decimal(preco_venda2)
            cleaned_data["preco_venda"] = preco_venda

        return cleaned_data
