from django import forms
from ..models import Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            "nome_empresa",
            "nro_cnpj",
            "razao_social",
            "nome_responsavel",
            "cargo",
            "email",
            "telefone",
            "nro_cpf",
        ]
        widgets = {
            "nome_empresa": forms.TextInput(
                attrs={"class": "form-control", "id": "nome_empresa"}
            ),
            "nro_cnpj": forms.TextInput(
                attrs={"class": "form-control cnpj-mask", "id": "nro_cnpj"}
            ),
            "razao_social": forms.TextInput(
                attrs={"class": "form-control", "id": "razao_social_empresa"}
            ),
            "nome_responsavel": forms.TextInput(
                attrs={"class": "form-control", "id": "nome_responsavel"}
            ),
            "cargo": forms.TextInput(
                attrs={"class": "form-control", "id": "cargo_responsavel"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "id": "email_responsavel"}
            ),
            "telefone": forms.TextInput(
                attrs={
                    "class": "form-control telefone-mask",
                    "id": "telefone_responsavel",
                }
            ),
            "nro_cpf": forms.TextInput(
                attrs={"class": "form-control cpf-mask", "id": "nro_cpf"}
            ),
        }
