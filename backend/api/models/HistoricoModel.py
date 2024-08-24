import uuid
from django.db import models
from .UsuarioModel import UsuarioModel
from .CustomModel import CustomModel
from api.utils import Utils


class HistoricoModel(CustomModel):
    id_historico = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    descricao = models.TextField(blank=True, null=True)
    usuario = models.UUIDField(UsuarioModel)
    class Meta:
        db_table = 'historico'

class HistoricoAlteracoesModel(CustomModel):
    id_historico = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    entidade = models.CharField(
        max_length=100
    ) 
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
        UsuarioModel, on_delete=models.SET_NULL, null=True
    )  # Usuário que realizou a alteração
    data_alteracao = models.DateTimeField(
        default=Utils.obter_data_hora_atual, editable=False
    )
    class Meta:
        db_table = 'historico_alteracoes'