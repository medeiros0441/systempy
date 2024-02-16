from django.db import models
from .empresa import Empresa


class Loja(models.Model):
    id_loja = models.AutoField(primary_key=True, db_column="id_loja")
    nome_loja = models.CharField(max_length=255, db_column="nome_loja")
    endereco = models.CharField(max_length=255, db_column="endereco", null=True)
    numero_telefone = models.CharField(
        max_length=15, db_column="numero_telefone", null=True
    )
    horario_operacao = models.CharField(
        max_length=50, db_column="horario_operacao", null=True
    )
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, db_column="fk_empresa"
    )
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "wms_loja"
