from django import forms
from ..models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nome_completo", "nivel_usuario", "status_acesso", "email", "senha"]
        labels = {
            "nome_completo": "Nome Responsável",
            "nivel_usuario": "Nível de Usuário",
            "status_acesso": "Status",
            "email": "E-mail do Responsável",
            "senha": "Senha",
        }
        widgets = {
            "nome_completo": forms.TextInput(
                attrs={"class": "form-control input", "required": "required"}
            ),
            "nivel_usuario": forms.Select(
                choices=[
                    (3, "colaborador"),
                    (2, "gerente"),
                ],
                attrs={"class": "form-select"},
            ),
            "status_acesso": forms.Select(
                choices=[(False, "Bloqueado"), (True, "Ativo")],
                attrs={"class": "form-select"},
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control input",
                    "oninput": "validarEmail()",
                }
            ),
            "senha": forms.PasswordInput(
                attrs={
                    "class": "form-control input",
                    "autocomplete": "off",
                    "oninput": "validarSenha()",
                }
            ),
        }
        # Defina o valor inicial padrão para os campos 'nivel_usuario' e 'status_acesso'
        initial = {"nivel_usuario": 2, "status_acesso": True}
