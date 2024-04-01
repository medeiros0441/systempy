from django.db import models
from .endereco import Endereco
from .empresa import Empresa
from django.utils import timezone
import uuid


class Cliente(models.Model):
    id_cliente = (
        models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False,
            null=True,
        ),
    )
    nome_cliente = models.CharField(max_length=255)
    telefone_cliente = models.CharField(max_length=20, null=True)
    ultima_compra = models.DateField(null=True, blank=True)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(null=True)
    tipo_cliente = models.CharField(max_length=50, null=True, blank=True)
    descricao_cliente = models.CharField(max_length=300, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
