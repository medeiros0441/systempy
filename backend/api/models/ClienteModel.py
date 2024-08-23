from .CustomModel import CustomModel
from django.db import models
from models import EnderecoModel,EmpresaModel
from django.utils import timezone
import uuid
from api.utils import Utils


class ClienteModel(CustomModel):
    id_cliente = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, null=True)
    ultima_compra = models.DateField(null=True, blank=True)
    tipo_cliente = models.CharField(max_length=50, null=True, blank=True)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    endereco = models.ForeignKey(EnderecoModel, on_delete=models.SET_NULL, null=True)
    empresa = models.ForeignKey(EmpresaModel, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'cliente'