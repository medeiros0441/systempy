from django.db import models
from django.utils import timezone
from .usuario import Usuario
import uuid

from ..utils import utils

class Sessao(models.Model):
    id_sessao = models.AutoField(
        primary_key=True,
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    ip_sessao = models.CharField(
        max_length=100,
    )
    descricao = models.CharField(
        null=True,
        max_length=200,
    )
    pagina_atual = models.CharField(
        null=True,
        max_length=200,
    )
    time_iniciou = models.DateTimeField(
        null=True,
        default=utils.obter_data_hora_atual(),
    )
    time_iniciou = models.DateTimeField(
        null=True,
        default=utils.obter_data_hora_atual(),
    )
    status = models.BooleanField(
        default=True,
    )
    insert = models.CharField(default=utils.obter_data_hora_atual(), editable=False,  max_length=100)
    update = models.CharField(default=utils.obter_data_hora_atual(), max_length=100)

    # Novos campos para dados de localização
    cidade = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    regiao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    pais = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    codigo_postal = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    organizacao = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
