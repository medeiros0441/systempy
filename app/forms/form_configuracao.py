from django import forms
from ..models import Configuracao


class ConfiguracaoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control input", "required": True, "maxlength": "255"}
            )
        self.fields["status_acesso"].widget.attrs = {}
    class Meta:
        model = Configuracao
        fields = [
            "usuario",
            "codigo",
            "titulo",
            "descricao",
            "descricao_interna",
            "status_acesso",
        ]
        labels = {
            "usuario": "Usuário",
            "codigo": "Código",
            "titulo": "Título",
            "descricao": "Descrição",
            "descricao_interna": "Descrição Interna",
            "status_acesso": "Status de Acesso",
        }
        widgets = {
            "status_acesso": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
