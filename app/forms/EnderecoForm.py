from django import forms
from ..models.endereco import Endereco


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ["rua", "numero", "cidade", "estado", "codigo_postal", "descricao"]

    def __init__(self, *args, **kwargs):
        super(EnderecoForm, self).__init__(*args, **kwargs)

        # Adiciona classes, atributos adicionais e limites de caracteres aos widgets dos campos
        self.fields["cidade"].widget.attrs["disabled"] = "disabled"
        self.fields["estado"].widget.attrs["disabled"] = "disabled"
        self.fields["codigo_postal"].widget.attrs[
            "class"
        ] = "form-control cep-mask input"
        self.fields["rua"].widget.attrs["maxlength"] = 255
        self.fields["numero"].widget.attrs["maxlength"] = 10
        self.fields["cidade"].widget.attrs["maxlength"] = 100
        self.fields["estado"].widget.attrs["maxlength"] = 50
        self.fields["codigo_postal"].widget.attrs["maxlength"] = 30
        self.fields["descricao"].widget.attrs[
            "maxlength"
        ] = None  # Remover essa linha se houver um limite específico para a descrição

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {
                    "class": "form-control input",
                    "required": "required",
                }
            )
