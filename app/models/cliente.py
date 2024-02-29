from django.db import models
from .endereco import Endereco
from django.utils import timezone


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True, db_column="id_cliente")
    nome_cliente = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    ultima_compra = models.DateField(null=True)
    insert = models.DateTimeField(db_column="date_time_insert",default=timezone.now)
    update = models.DateTimeField(db_column="date_time_update", null=True)
    tipo_cliente = models.CharField(max_length=50,null=True)
    descricao_cliente = models.CharField(max_length=300,null=True)
    endereco = models.ForeignKey(
        Endereco, on_delete=models.CASCADE, db_column="fk_endereco"
    )

    class Meta:
        db_table = "wms_cliente"
