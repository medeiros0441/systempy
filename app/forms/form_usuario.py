from django import forms
from ..models import Usuario


class UsuarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['nome_completo'].widget.attrs.update({'class': 'form-control input', 'required': 'required'})
        self.fields['nivel_usuario'].widget.attrs.update({'class': 'form-control'})
        self.fields['status_acesso'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control input', 'type': 'email'})
        self.fields['senha'].widget.attrs.update({'class': 'form-control input', 'type': 'password', 'autocomplete': 'off', 'oninput': 'validarSenha()'})

    class Meta:
        model = Usuario
        fields = ['nome_completo', 'nivel_usuario', 'status_acesso', 'email', 'senha']
        labels = {
            'nome_completo': 'Nome Responsável',
            'nivel_usuario': 'Nível de Usuário',
            'status_acesso': 'Status',
            'email': 'E-mail do Responsável',
            'senha': 'Senha',
        }
        widgets = {
            'status_acesso': forms.Select(choices=((True, 'Ativo'), (False, 'Bloqueado'))),
        }