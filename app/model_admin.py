from django.db import models
from models.empresa import Empresa


class PlanoGestao(models.Model):
    id_plano_gestao = models.AutoField(primary_key=True, db_column="id_plano_gestao")
    nome = models.CharField(max_length=100, db_column="nome_plano_gestao")
    descricao = models.CharField(
        max_length=500, db_column="descricao_plano_gestao", null=True, blank=True
    )
    preco = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="preco_plano_gestao"
    )
    duracao_meses = models.IntegerField(db_column="duracao_meses_plano_gestao")
    status = models.BooleanField(db_column="status_plano_gestao", default=True)
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "smw_plano_gestao"


class InscricaoGestao(models.Model):
    id_inscricao_gestao = models.AutoField(
        primary_key=True, db_column="id_inscricao_gestao"
    )
    nome = models.CharField(max_length=50, db_column="nome_inscricao")
    descricao = models.CharField(max_length=255, db_column="descricao_inscricao")
    preco = models.FloatField(db_column="preco_inscricao")
    periodo_faturamento = models.IntegerField(db_column="periodo_faturamento_inscricao")
    status = models.BooleanField(db_column="status_inscricao")
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)
    plano_gestao = models.ForeignKey(
        PlanoGestao, on_delete=models.CASCADE, db_column="fk_plano_gestao"
    )
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, db_column="fk_empresa"
    )

    class Meta:
        db_table = "smw_inscricao_gestao"


class HistoricoCliente(models.Model):
    id_historico = models.AutoField(primary_key=True, db_column="id_historico_cliente")
    data_evento = models.DateTimeField(db_column="data_evento")
    descricao_evento = models.CharField(max_length=500, db_column="descricao_evento")
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        db_column="fk_empresa",
    )

    class Meta:
        db_table = "smw_historico_cliente"


class ConfiguracaoPlataforma(models.Model):
    id_configuracao_plataforma = models.AutoField(
        primary_key=True, db_column="id_configuracao_plataforma"
    )
    nome = models.CharField(max_length=100, db_column="nome_configuracao_plataforma")
    valor = models.CharField(max_length=500, db_column="valor_configuracao_plataforma")
    status = models.BooleanField(db_column="status_configuracao_plataforma")
    descricao = models.CharField(
        max_length=500, db_column="descricao_configuracao_plataforma"
    )
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        db_column="dk_empresa",
    )

    class Meta:
        db_table = "smw_configuracao_plataforma"


class Sessao(models.Model):
    id_sessao = models.AutoField(primary_key=True, db_column="id_sessao")
    hora_inicio = models.DateTimeField(db_column="hora_inicio_sessao")
    hora_fim = models.DateTimeField(db_column="hora_fim_sessao", null=True)
    navegador = models.CharField(max_length=255, db_column="navegador_sessao")
    status = models.BooleanField(db_column="status_sessao")
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "smw_historico_cliente"


class Registro(models.Model):
    id_registro = models.AutoField(primary_key=True, db_column="id_registro")
    texto = models.TextField(db_column="texto")
    codigo_localidade_texto = models.TextField(db_column="codigo_localidade_texto")
    sistema_texto = models.TextField(db_column="sistema_texto")
    nivel = models.CharField(max_length=255, db_column="nivel")
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)
    sessao = models.ForeignKey(
        Sessao,
        on_delete=models.CASCADE,
        related_name="registros",
        db_column="fk_sessao",
    )

    class Meta:
        db_table = "smw_registro"
