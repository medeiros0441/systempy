from django.db import models
from .cliente import Cliente
from .venda import Venda
from django.utils import timezone


class Galao(models.Model):
    id_galao = models.AutoField(primary_key=True, db_column="id_galao")
    data_insercao = models.DateTimeField()
    data_atualizacao = models.DateTimeField(null=True)
    data_validade = models.CharField(max_length=50)
    data_fabricacao = models.CharField(max_length=50)
    descricao = models.TextField(null=True)
    id_galao = models.AutoField(primary_key=True, db_column="id_galao")
    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "smw_galao"


class GestaoGalao(models.Model):
    id_gestao_galao = models.AutoField(primary_key=True, db_column="id_gestao_galao")
    fk_galao_saiu = models.ForeignKey(
        Galao,
        on_delete=models.CASCADE,
        db_column="fk_galao_saiu",
        related_name="galao_saiu_set",
        null=True,
    )
    fk_galao_entrando = models.ForeignKey(
        Galao,
        on_delete=models.CASCADE,
        db_column="fk_galao_entrando",
        related_name="galao_entrando_set",
        null=True,
    )
    fk_cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, db_column="fk_cliente", null=True
    )
    fk_venda = models.ForeignKey(
        Venda, on_delete=models.CASCADE, db_column="fk_venda", null=True
    )
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "smw_gestaogalao"
