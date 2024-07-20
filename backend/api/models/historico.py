import uuid
from django.db import models
from ..models.usuario import Usuario
from django.utils import timezone

from api.utils import Utils


class Historico(models.Model):
    id_historico = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    descricao = models.TextField(blank=True, null=True)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    usuario = models.UUIDField(
        Usuario,
    )


class HistoricoAlteracoes(models.Model):
    id_historico = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    entidade = models.CharField(
        max_length=100
    )  # Nome da entidade alterada, ex: 'PDV', 'AssociadoPDV'
    entidade_id = models.UUIDField()  # ID da entidade alterada
    tipo_alteracao = models.CharField(
        max_length=50
    )  # Tipo de alteração, ex: 'criação', 'atualização', 'exclusão'
    campo_alterado = models.CharField(
        max_length=100, null=True, blank=True
    )  # Nome do campo alterado
    valor_antigo = models.TextField(null=True, blank=True)  # Valor antigo do campo
    valor_novo = models.TextField(null=True, blank=True)  # Valor novo do campo
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True
    )  # Usuário que realizou a alteração
    data_alteracao = models.DateTimeField(
        default=Utils.obter_data_hora_atual, editable=False
    )

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)
