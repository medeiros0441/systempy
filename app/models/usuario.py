from django.db import models
from django.utils import timezone
import uuid
from app.utils import Utils
from .empresa import Empresa


class Usuario(models.Model):
    id_usuario = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    nome_completo = models.CharField(
        max_length=255,
    )
    nome_usuario = models.CharField(
        max_length=50,
    )
    senha = models.CharField(
        max_length=200,
    )
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    nivel_usuario = models.IntegerField()
    status_acesso = models.BooleanField(
        default=False,
    )

    email = models.EmailField(
        max_length=255,
    )
    ultimo_login = models.DateTimeField(null=True)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)


class Personalizacao(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    chave = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    descricao_interna = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)
