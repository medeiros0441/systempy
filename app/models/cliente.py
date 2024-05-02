from django.db import models
from .endereco import Endereco
from .empresa import Empresa
from django.utils import timezone
import uuid

from ..utils import utils
class Cliente(models.Model):
    id_cliente = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    nome_cliente = models.CharField(max_length=255)
    telefone_cliente = models.CharField(max_length=20, null=True)
    ultima_compra = models.DateField(null=True, blank=True)
    insert = models.CharField(default=utils.obter_data_hora_atual(), editable=False,  max_length=100)
    update = models.CharField(default=utils.obter_data_hora_atual(), max_length=100)
    tipo_cliente = models.CharField(max_length=50, null=True, blank=True)
    descricao_cliente = models.CharField(max_length=300, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
