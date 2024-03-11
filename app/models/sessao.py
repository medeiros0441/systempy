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

    # Novos campos para dados de localização
    cidade = models.CharField(max_length=100, blank=True, null=True, db_column="cidade")
    regiao = models.CharField(max_length=100, blank=True, null=True, db_column="regiao")
    pais = models.CharField(max_length=100, blank=True, null=True, db_column="pais")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, db_column="latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, db_column="longitude")
    codigo_postal = models.CharField(max_length=20, blank=True, null=True, db_column="codigo_postal")
    organizacao = models.CharField(max_length=200, blank=True, null=True, db_column="organizacao")
    
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column="fk_usuario", null=True
    )

    class Meta:
        db_table = "wms_sessao"
