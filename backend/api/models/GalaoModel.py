
from django.db import models
from api.models import CustomModel,VendaModel,LojaModel


class GalaoModel(CustomModel):
    id_galao = models.AutoField(primary_key=True)
    data_validade = models.CharField(max_length=50, null=True)
    data_fabricacao = models.CharField(max_length=50, null=True)
    descricao = models.TextField(null=True)
    quantidade = models.IntegerField(default=0)  # Quantidade de galões
    titulo = models.CharField(max_length=100, null=True)  # Título do galão
    loja = models.ForeignKey(LojaModel, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'galao'

class GestaoGalaoModel(CustomModel):
    id_gestao_galao = models.AutoField(
        primary_key=True,
    )
    galao_saiu = models.ForeignKey(
        GalaoModel,
        on_delete=models.CASCADE,
        related_name="galao_saiu_set",
        null=True,
    )
    galao_entrando = models.ForeignKey(
        GalaoModel,
        on_delete=models.CASCADE,
        related_name="galao_entrando_set",
        null=True,
    )
    venda = models.ForeignKey(VendaModel, on_delete=models.CASCADE, null=True)
    descricao = models.TextField(null=True)
    class Meta:
        db_table = 'gestao_galao'