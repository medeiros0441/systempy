from django import forms
from ..models.loja import Loja

class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = [
            'nome_loja',
            'numero_telefone',
            'horario_operacao',
            'empresa',
            'endereco'
        ]

    def __init__(self, *args, **kwargs):
        super(LojaForm, self).__init__(*args, **kwargs)

        # Adicione classes CSS ou outros atributos conforme necessário para estilização
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
