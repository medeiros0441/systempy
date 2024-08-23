from django.http import JsonResponse
from functools import wraps
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    FieldDoesNotExist,
)
from datetime import datetime
from pytz import timezone
import random
import string
from decimal import Decimal
import json
from django.forms.models import model_to_dict
import uuid
import logging
from django.db.models import Model, ForeignKey
import re
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from django.http import HttpResponse

class Utils:
    
    @staticmethod
    def set_cookie(response: HttpResponse, key: str, value: str, days_expire: int = 7):
        # Calcula a data de expiração com base em days_expire
        expires = datetime.utcnow() + timedelta(days=days_expire)
        
        # Define o cookie com os parâmetros fornecidos
        response.set_cookie(
            key,                        # Nome do cookie
            value,                      # Valor do cookie
            max_age=days_expire * 24 * 60 * 60,  # Tempo de expiração em segundos
            expires=expires,            # Data e hora de expiração
            path='/',                   # Caminho onde o cookie é válido
            domain=None,                # Domínio onde o cookie é válido
            secure=False,               # Se True, o cookie só será enviado via HTTPS
            httponly=False,             # Se True, o cookie não será acessível via JavaScript
            samesite='Lax'              # Política de SameSite do cookie (Lax, Strict ou None)
        )
        
        return response

    @staticmethod
    def get_cookie(request, key):
        return request.COOKIES.get(key)
    
    @staticmethod
    def is_valid_email(value):
        """Valida se o email é válido."""
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(value)
            return True
        except ValidationError:
            return False

    @staticmethod
    def is_valid_cpf(value):
        """Valida se o CPF é válido."""
        if re.match(r'^\d{11}$', value):
            # Lógica básica para validar CPF
            # Considerar usar uma biblioteca específica para validação de CPF
            return True
        return False

    @staticmethod
    def is_valid_cnpj(value):
        """Valida se o CNPJ é válido."""
        if re.match(r'^\d{14}$', value):
            # Lógica básica para validar CNPJ
            # Considerar usar uma biblioteca específica para validação de CNPJ
            return True
        return False

    @staticmethod
    def is_valid_phone(value):
        """Valida se o telefone é válido."""
        return re.match(r'^\d{10,15}$', value) is not None
    
    def converter_para_decimal(valor):
        try:
            if valor is None or valor == "":
                return Decimal(0)
            elif valor == "NaN":
                return Decimal(0)
            elif "," in valor:
                # Se houver vírgula no valor, substituímos por ponto e convertemos para Decimal
                valor = valor.replace(",", ".")
                return Decimal(valor)
            else:
                return Decimal(valor)
        except (ValueError, TypeError):
            return Decimal(0)

    @staticmethod
    def obter_data_hora_atual(value=None):
        # Obtém a data e hora atual no fuso horário do Brasil
        brasil_tz = timezone("America/Sao_Paulo")
        dt_brasil = datetime.now(brasil_tz)

        # Formata a data e hora de acordo com o parâmetro especificado
        if value == True or value == "date":
            # Retorna apenas a data no formato dia/mes/ano
            return dt_brasil.strftime("%d/%m/%Y")
        elif value == False or value == "time":
            return dt_brasil.strftime("%H:%M")
        else:
            # Retorna data e hora no formato dia/mes/ano hora:minutos
            return dt_brasil.strftime("%d/%m/%Y %H:%M")

    

    def gerar_numero_aleatorio(tamanho=4):
        # Gerar um número aleatório com 'tamanho' dígitos
        return "".join(random.choices(string.digits, k=tamanho))

    def obter_dados_localizacao_ipinfo(ip, requests):
        # Chave de API do ipinfo.io
        api_key = "7a622c40229db0"

        # URL da API ipinfo.io
        url = f"http://ipinfo.io/{ip}?token={api_key}"

        try:
            # Fazendo uma solicitação GET para a API ipinfo.io
            response = requests.get(url)
            from api.models import Sessao

            # Verifica se a solicitação foi bem-sucedida (código de status HTTP 200)
            if response.status_code == 200:
                # Parseia os dados JSON da resposta
                data = response.json()
                sessao = Sessao.objects.create(
                    ip_sessao=ip,
                    cidade=data.get("city"),
                    regiao=data.get("region"),
                    pais=data.get("country"),
                    latitude=float(data.get("loc", "").split(",")[0]),
                    longitude=float(data.get("loc", "").split(",")[1]),
                    codigo_postal=data.get("postal"),
                    organizacao=data.get("org"),
                )

            else:
                # Se a solicitação falhar, imprime o status da resposta
                print(f"Erro: {response.status_code}")

        except Exception as e:
            print(f"Erro ao obter dados de localização: {e}")

    def configuracao_usuario(request, id_usuario, codigo):
        from api.views.ErroView import ErroView
        from api.models import Configuracao

        try:
            configuracao = Configuracao.objects.get(
                usuario_id=id_usuario, codigo=codigo
            )
            if not configuracao.status_acesso:
                mensagem = (
                    "Acesso negado: você não tem permissão para executar o método."
                )
                return False, ErroView.erro(request, mensagem)
            else:
                return True, None
        except ObjectDoesNotExist:
            mensagem = "Configuração não encontrada."
            return False, ErroView.erro(request, mensagem)
        except MultipleObjectsReturned:
            mensagem = "Ocorreu um erro inesperado. Por favor, entre em contato com a equipe de suporte."
            return False, ErroView.erro(request, mensagem)

  
    def lista_de_configuracao():
        return [
            {"nome": "Usuario", "codigo": 1},
            {"nome": "Empresa", "codigo": 2},
            {"nome": "Endereco", "codigo": 3},
            {"nome": "Galao", "codigo": 4},
            {"nome": "Loja", "codigo": 5},
            {"nome": "Produto", "codigo": 6},
            {"nome": "Venda", "codigo": 7},
            {"nome": "Cliente", "codigo": 8},
            {"nome": "Motoboy", "codigo": 9},
            {"nome": "Pdv", "codigo": 10},
            {"nome": "TransacaoPDV", "codigo": 11},
            {"nome": "RegistroDiarioPDV", "codigo": 12},
            {"nome": "Faturamento", "codigo": 13},
        ]

    def buscar_nome_por_codigo(codigo_classe):
        for configuracao in Utils.lista_de_configuracao():
            if configuracao["codigo"] == codigo_classe:
                return configuracao["nome"]
        return None

    def extract_data_to_model_instance(model_class, data, instance=None):
        """
        Extrai dados de um dicionário e os atribui a uma instância do modelo fornecido.

        Args:
            model_class (Model): A classe do modelo Django.
            data (dict): O dicionário de dados do qual extrair os valores.
            instance (Model, optional): A instância do modelo para atualizar. Se None, uma nova instância será criada.

        Returns:
            Model: Uma instância do modelo com os dados extraídos.
        """
        if not issubclass(model_class, Model):
            raise ValueError(
                "O argumento 'model_class' deve ser uma classe de modelo Django."
            )

        if instance is None:
            instance = model_class()

        for field in model_class._meta.get_fields():
            field_name = field.name
            if field_name in data:
                setattr(instance, field_name, data[field_name])
            elif isinstance(field, ForeignKey) and field_name + "_id" in data:
                setattr(instance, field_name + "_id", data[field_name + "_id"])

        return instance

    def modelo_para_json(*instances):
        """
        Converte várias instâncias de modelos Django para um dicionário JSON agrupado.
        """

        def instance_to_dict(instance):
            if instance is None:
                return {}

            try:
                # Converte a instância para um dicionário, incluindo todos os campos
                data = model_to_dict(
                    instance, fields=[field.name for field in instance._meta.fields]
                )

                # Adiciona a chave primária manualmente, caso não tenha sido incluída
                pk_name = instance._meta.pk.name
                if pk_name not in data:
                    data[pk_name] = str(getattr(instance, pk_name))

                # Adiciona campos de ForeignKey representadas por _id
                for field in instance._meta.fields:
                    if isinstance(field, ForeignKey):
                        related_instance = getattr(instance, field.name)
                        if related_instance:
                            data[field.name + "_id"] = str(related_instance.pk)

                return data
            except Exception as e:
                return {"error": str(e)}

        combined_data = {}
        for instance in instances:
            if instance:
                instance_name = instance.__class__.__name__.lower()
                combined_data[instance_name] = instance_to_dict(instance)
        return combined_data

    def modelos_para_lista_json(instances):
        """
        Converte uma lista de instâncias de um modelo Django para uma lista de dicionários JSON.
        """
        return [Utils.modelo_para_json(instance) for instance in instances]
