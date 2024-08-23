from django.db import models
from models import UsuarioModel,CustomModel
import uuid


class SessaoModel(CustomModel):
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
    )
    status = models.BooleanField(
        default=True,
    )

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

    usuario = models.ForeignKey(UsuarioModel, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table ="sessao"