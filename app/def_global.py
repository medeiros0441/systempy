from django.shortcuts import render, redirect
from .models.usuario import Usuario

from .models.empresa import Empresa


def criar_alerta_js(texto):
    # Modelo do script JavaScript que será retornado
    script = script_js(f"""  alertCustomer('{texto}');""")
    return script


def script_js(function):
    # Modelo do script JavaScript que será retornado
    script = f"""
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            {function}
        }});
    </script>
    """
    return script


import random
import string


def erro(request, error_message):
    return render(request, "Erro.html", {"error_message": error_message})


def gerar_numero_aleatorio(tamanho=4):
    # Gerar um número aleatório com 'tamanho' dígitos
    return "".join(random.choices(string.digits, k=tamanho))


def email_existe(email):
    return Usuario.objects.filter(email=email).exists()


def usuario_existe(usuario):
    return Usuario.objects.filter(nome_usuario=usuario).exists()


def telefone_existe(telefone):
    return Empresa.objects.filter(telefone=telefone).exists()


def cpf_existe(cpf):
    Empresa.objects.filter(nro_cpf=cpf).exists()
    return


def cnpj_existe(cnpj):
    return Empresa.objects.filter(nro_cnpj=cnpj).exists()
