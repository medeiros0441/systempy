from django import forms
from ..models import Venda, Loja, Cliente, Associado
from ..static import UserInfo


class VendaForm(forms.ModelForm):
    # Definir as opções para forma de pagamento e estado da transação
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
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    valor_pago = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    troco = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    nota_fiscal = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

   
    descricao = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": "5"}))
    loja = forms.ModelChoiceField(
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
        if id_usuario is not None:
            self.fields["usuario"].widget = forms.NumberInput(
                attrs={"class": "form-control", "value": id_usuario}
            )
            # Filtrar as associações do usuário com acesso ativo
            associacoes = Associado.objects.filter(
                usuario_id=id_usuario, status_acesso=True
            )
            # Obter as lojas associadas
            lojas_disponiveis = [associacao.loja for associacao in associacoes]
            # Configurar as opções do campo 'loja'
            if len(lojas_disponiveis) == 1:
                self.fields["loja"].widget.choices = [
                    (loja.id_loja, loja.nome_loja) for loja in lojas_disponiveis
                ]
            else:
                self.fields["loja"].widget.choices = [("", "Selecione")] + [
                    (loja.id_loja, loja.nome_loja) for loja in lojas_disponiveis
                ]
        else:
            # Se o id_usuario não estiver definido, configurar uma opção padrão para 'loja'
            self.fields["loja"].widget.choices = [("", "ID de usuário não fornecido")]
