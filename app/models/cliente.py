from django.db import models
from .endereco import Endereco


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True, db_column="id_cliente")
    nome_cliente = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    ultima_compra = models.DateField()
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)
    tipo_cliente = models.CharField(max_length=50)
    fk_endereco = models.ForeignKey(
        Endereco, on_delete=models.CASCADE, db_column="fk_endereco"
    )
   
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "smw_cliente"
