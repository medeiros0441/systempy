from django.db import models
import uuid

from .CustomModel import CustomModel  
class EmpresaModel(CustomModel):
    id_empresa = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    nome_empresa = models.TextField()
    nro_cnpj = models.TextField()
    razao_social = models.TextField(blank=True, null=True)
    descricao = models.TextField(null=True)
    nome_responsavel = models.TextField()
    cargo = models.TextField()
    email = models.EmailField()
    nro_cpf = models.TextField()
    telefone = models.TextField()
    class Meta:
        db_table = 'empresa'