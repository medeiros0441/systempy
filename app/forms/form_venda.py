from django import forms
from ..models import Venda, Loja, Associado


class VendaForm(forms.ModelForm):
    FORMA_PAGAMENTO_CHOICES = [
        ("0", "Selecione"),
        ("pix", "Pix"),
        ("cartao_credito", "Cartão de Crédito"),
        ("cartao_debito", "Cartão de Débito"),
        ("fiado", "Fiado"),
        ("dinheiro", "Dinheiro"),
    ]

    ESTADO_TRANSACAO_CHOICES = [
        ("0", "Selecione"),
        ("finalizado", "Finalizado"),
        ("processando", "Processando"),
        ("pendente", "Pendente"),
    ]

    METODO_ENTREGA_CHOICES = [
        ("0", "Selecione"),
        ("retirado_na_loja", "Retirado na Loja"),
        ("entrega_no_local", "Entrega no Local"),
    ]

    estado_transacao = forms.ChoiceField(
        choices=ESTADO_TRANSACAO_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    metodo_entrega = forms.ChoiceField(
        choices=METODO_ENTREGA_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    valor_total = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control money-mask"}),
    )
    valor_pago = forms.DecimalField(
        max_digits=10,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control money-mask"}),
    )
    troco = forms.DecimalField(
        max_digits=10,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control money-mask"}),
    )
    nota_fiscal = forms.DecimalField(
        max_digits=10,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    descricao = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
    )
    loja = forms.ModelChoiceField(
        required=False,
        queryset=Loja.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    forma_pagamento = forms.ChoiceField(
        choices=FORMA_PAGAMENTO_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Venda
        fields = "__all__"

    def __init__(self, id_usuario=None, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)
        self.set_loja_choices(id_usuario)

    def set_loja_choices(self, id_usuario):
        if id_usuario is not None:
            self.fields["usuario"].widget = forms.NumberInput(
                attrs={"class": "form-control", "value": id_usuario}
            )
            associacoes = Associado.objects.filter(
                usuario_id=id_usuario, status_acesso=True
            )
            lojas_disponiveis = [associacao.loja for associacao in associacoes]
            loja_choices = [
                (loja.id_loja, loja.nome_loja) for loja in lojas_disponiveis
            ]
            if len(loja_choices) > 1:
                loja_choices.insert(0, ("0", "Selecione"))
            self.fields["loja"].widget.choices = loja_choices
        else:
            self.fields["loja"].widget.choices = [("", "ID de usuário não fornecido")]
