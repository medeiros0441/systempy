from django.db import models
from django.utils import timezone


class Endereco(models.Model):
    id_endereco = models.AutoField(primary_key=True, db_column="id_endereco")
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10, null=True, blank=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=30)
    descricao = models.TextField()
    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "wms_endereco"
