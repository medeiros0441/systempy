from django.db import models
from .empresa import Empresa
from django.utils import timezone


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_column="id_usuario")
    nome_completo = models.CharField(max_length=255, db_column="nome_completo")
    nome_usuario = models.CharField(max_length=50, db_column="nome_usuario")
    senha = models.CharField(max_length=50, db_column="senha")
    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(db_column="date_time_update", null=True)
    nivel_usuario = models.IntegerField(db_column="nivel_usuario")
    status_acesso = models.CharField(
        max_length=20, db_column="status_acesso", null=True
    )
    email = models.EmailField(max_length=255, db_column="email")
    ultimo_login = models.DateTimeField(db_column="ultimo_login", null=True)
    fk_empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, db_column="fk_empresa"
    )

    @property
    def primeiro_nome(self):
        # Separar o nome completo em partes usando espaços como delimitadores
        partes_nome = self.nome_completo.split()

        # Retorna apenas o primeiro nome, se houver, caso contrário, retorna uma string vazia
        return partes_nome[0] if partes_nome else ""

    class Meta:
        db_table = "smw_usuario"
