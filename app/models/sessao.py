from django.db import models
from django.utils import timezone
from .usuario import Usuario
import uuid


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
        default=timezone.now,
    )
    time_iniciou = models.DateTimeField(
        null=True,
        default=timezone.now,
    )
    status = models.BooleanField(
        default=True,
    )
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(null=True)

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
