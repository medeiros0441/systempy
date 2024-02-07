from django.db import models
from django.utils import timezone


class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True, db_column="id_empresa")
    nome_empresa = models.TextField(db_column="nome_empresa")
    nro_cnpj = models.TextField(db_column="nro_cnpj_empresa")
    razao_social = models.TextField(
        db_column="razao_social_empresa", blank=True, null=True
    )
    descricao = models.TextField(db_column="descricao_empresa", null=True)
    nome_responsavel = models.TextField(db_column="nome_responsavel")
    cargo = models.TextField(db_column="cargo_responsavel")
    email = models.EmailField(db_column="email_responsavel")
    nro_cpf = models.TextField(db_column="nro_cpf_responsavel")
    telefone = models.TextField(db_column="telefone_responsavel")
    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "smw_empresa"
