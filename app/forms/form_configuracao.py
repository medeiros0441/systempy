from django import forms
from ..models import Configuracao


class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracao
        fields = ["usuario", "descricao", "status"]

    def __init__(self, *args, **kwargs):
        super(ConfiguracaoForm, self).__init__(*args, **kwargs)
        # Adiciona classes CSS aos widgets
        self.fields["usuario"].widget.attrs.update({"class": "form-control"})
        self.fields["descricao"].widget.attrs.update({"class": "form-control"})
        self.fields["status"].widget.attrs.update({"class": "form-check-input"})
