from django.db import models
from django.utils import timezone
import uuid


class Endereco(models.Model):
    id_endereco = models.AutoField(primary_key=True, db_column="id_endereco")

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    rua = models.CharField(max_length=255, db_column="rua")
    numero = models.CharField(db_column="numero", max_length=10, null=True, blank=True)
    bairro = models.CharField(db_column="bairro", max_length=100)
    cidade = models.CharField(db_column="cidade", max_length=100)
    estado = models.CharField(db_column="estado", max_length=50)
    codigo_postal = models.CharField(db_column="codigo_postal", max_length=30)
    descricao = models.TextField(db_column="descricao", null=True, max_length=500)
    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "wms_endereco"
