from django.db import models
from django.utils import timezone
from .usuario import Usuario


class Sessao(models.Model):
    id_sessao = models.AutoField(primary_key=True, db_column="id_sessao")
    ip_sessao = models.CharField(max_length=100, db_column="ip_sessao")
    descricao = models.CharField(max_length=100, db_column="descricao")
    pagina_atual = models.CharField(max_length=200, db_column="pagina_atual")
    time_iniciou = models.DateTimeField(default=timezone.now, db_column="time_iniciou")
    time_iniciou = models.DateTimeField(
        default=timezone.now, db_column="time_finalizou"
    )
    status = models.BooleanField(default=True, db_column="status")
    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(db_column="date_time_update", null=True)

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column="fk_usuario"
    )

    class Meta:
        db_table = "wms_sessao_usuario"
