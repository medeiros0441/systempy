# forms.py
from django import forms
from models.usuario import Usuario, Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = "__all__"


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
