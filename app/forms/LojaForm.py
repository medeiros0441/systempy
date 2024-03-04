from django import forms
from ..models.loja import Loja


class LojaForm(forms.ModelForm):
    segunda = forms.BooleanField(label="Segunda-feira", required=False)
    terca = forms.BooleanField(label="Terça-feira", required=False)
    quarta = forms.BooleanField(label="Quarta-feira", required=False)
    quinta = forms.BooleanField(label="Quinta-feira", required=False)
    sexta = forms.BooleanField(label="Sexta-feira", required=False)
    sabado = forms.BooleanField(label="Sábado", required=False)
    domingo = forms.BooleanField(label="Domingo", required=False)

    class Meta:
        model = Loja
        fields = [
            "nome_loja",
            "numero_telefone",
            "horario_operacao_inicio",
            "horario_operacao_fim",
            "segunda",
            "terca",
            "quarta",
            "quinta",
            "sexta",
            "sabado",
            "domingo",
            "empresa",
            "endereco",
        ]

    def __init__(self, *args, **kwargs):
        super(LojaForm, self).__init__(*args, **kwargs)
        # Adiciona classes CSS aos campos do formulário
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"

        # Adiciona etiquetas flutuantes para os campos de horário
        self.fields["numero_telefone"].widget.attrs["class"] = "form-control mask-telefone"
        self.fields["horario_operacao_inicio"].widget.attrs["type"] = "time"
        self.fields["horario_operacao_inicio"].widget.attrs[
            "id"
        ] = "horario_operacao_inicio"
        self.fields["horario_operacao_inicio"].widget.attrs[
            "name"
        ] = "horario_operacao_inicio"

        self.fields["horario_operacao_fim"].widget.attrs["type"] = "time"
        self.fields["horario_operacao_fim"].widget.attrs["id"] = "horario_operacao_fim"
        self.fields["horario_operacao_fim"].widget.attrs[
            "name"
        ] = "horario_operacao_fim"

        # Adiciona as classes form-check e form-check-inline aos campos de checkbox
        for field_name in [
            "segunda",
            "terca",
            "quarta",
            "quinta",
            "sexta",
            "sabado",
            "domingo",
        ]:
            self.fields[field_name].widget.attrs[
                "class"
            ] = "form-check form-check-inline"
