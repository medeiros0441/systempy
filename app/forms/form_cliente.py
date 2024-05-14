from django import forms
from ..models import Cliente, Endereco, Empresa
from .form_endereco import EnderecoForm
from .form_empresa import EmpresaForm


class ClienteForm(forms.ModelForm):
    endereco = EnderecoForm()  # Instância do formulário de Endereco
    empresa = EmpresaForm()  # Instância do formulário de Empresa

    class Meta:
        model = Cliente
        fields = [
            "nome",
            "telefone",
            "ultima_compra",
            "tipo_cliente",
            "descricao",
            "endereco",
            "empresa",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "required": False}),
            "telefone": forms.TextInput(
                attrs={"class": "form-control telefone-mask", "required": False}
            ),
            "ultima_compra": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "required": False}
            ),
            "tipo_cliente": forms.TextInput(
                attrs={"class": "form-control", "required": False}
            ),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "required": False}
            ),
            # 'endereco' e 'empresa' são tratados automaticamente pelos subformulários
        }

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        if "instance" in kwargs:
            self.fields["endereco"] = EnderecoForm(instance=kwargs["instance"].endereco)
            self.fields["empresa"] = EmpresaForm(instance=kwargs["instance"].empresa)

    def save(self, commit=True):
        endereco_instance = self.fields["endereco"].save(commit=False)
        empresa_instance = self.fields["empresa"].save(commit=False)

        if commit:
            endereco_instance.save()
            empresa_instance.save()

        cliente_instance = super(ClienteForm, self).save(commit=False)
        cliente_instance.endereco = endereco_instance
        cliente_instance.empresa = empresa_instance

        if commit:
            cliente_instance.save()

        return cliente_instance
