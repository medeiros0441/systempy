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
            "nome_cliente",
            "telefone_cliente",
            "ultima_compra",
            "tipo_cliente",
            "descricao_cliente",
            "endereco",
            "empresa",
        ]
        widgets = {
            "nome_cliente": forms.TextInput(attrs={"class": "form-control"}),
            "telefone_cliente": forms.TextInput(attrs={"class": "form-control"}),
            "ultima_compra": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "tipo_cliente": forms.TextInput(attrs={"class": "form-control"}),
            "descricao_cliente": forms.Textarea(attrs={"class": "form-control"}),
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
