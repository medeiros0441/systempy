from django.db import models
from .empresa import Empresa
from .endereco import Endereco
from django.utils import timezone


class Loja(models.Model):
    id_loja = models.AutoField(primary_key=True, db_column="id_loja")
    nome_loja = models.CharField(max_length=255, db_column="nome_loja")
    numero_telefone = models.CharField(
        max_length=50, db_column="numero_telefone", null=True
    )

    horario_operacao_inicio = models.TimeField(
        null=True, blank=True, db_column="horario_operacao_inicio"
    )
    horario_operacao_fim = models.TimeField(
        null=True, blank=True, db_column="horario_operacao_fim"
    )
    segunda = models.BooleanField(default=False, db_column="segunda")
    terca = models.BooleanField(default=False, db_column="terca")
    quarta = models.BooleanField(default=False, db_column="quarta")
    quinta = models.BooleanField(default=False, db_column="quinta")
    sexta = models.BooleanField(default=False, db_column="sexta")
    sabado = models.BooleanField(default=False, db_column="sabado")
    domingo = models.BooleanField(default=False, db_column="domingo")

    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(db_column="date_time_update", null=True)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, db_column="fk_empresa"
    )
    endereco = models.ForeignKey(
        Endereco, on_delete=models.CASCADE, db_column="fk_endereco", null=True
    )

    class Meta:
        db_table = "wms_loja"
