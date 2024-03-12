from django.db import models
from .empresa import Empresa
from django.utils import timezone
import uuid


class Usuario(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    id_usuario = models.AutoField(
        primary_key=True,
    )
    nome_completo = models.CharField(
        max_length=255,
    )
    nome_usuario = models.CharField(
        max_length=50,
    )
    senha = models.CharField(
        max_length=200,
    )
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(null=True)
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

    @property
    def primeiro_nome(self):
        # Separar o nome completo em partes usando espaços como delimitadores
        partes_nome = self.nome_completo.split()

        # Retorna apenas o primeiro nome, se houver, caso contrário, retorna uma string vazia
        return partes_nome[0] if partes_nome else ""
