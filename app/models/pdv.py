import uuid
from django.utils import timezone
from app.utils import Utils
from django.db import models
from .usuario import Usuario
from .loja import Loja
from .venda import Venda


class PDV(models.Model):
    EXCLUIDO = 0
    ABERTO = 1
    FECHADO = 2
    BLOQUEADO = 3

    STATUS_OPERACAO_CHOICES = [
        (BLOQUEADO, "Bloqueado"),
        (EXCLUIDO, "Excluído"),
        (ABERTO, "Aberto"),
        (FECHADO, "Fechado"),
    ]

    id_pdv = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255, null=True)
    loja = models.ForeignKey("Loja", on_delete=models.CASCADE)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    saldo_inicial = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )
    status_operacao = models.IntegerField(
        choices=STATUS_OPERACAO_CHOICES, default=FECHADO
    )

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class RegistroDiarioPDV(models.Model):
    id_registro_diario = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    pdv = models.ForeignKey(PDV, on_delete=models.CASCADE, editable=False)
    dia = models.CharField(
        editable=False, null=True, max_length=50, default=Utils.obter_data_hora_atual
    )
    saldo_inicial_dinheiro = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0, null=True
    )
    saldo_final_dinheiro = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    saldo_final_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    maquina_tipo = models.CharField(max_length=50, null=True, blank=True)
    saldo_final_maquina = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    horario_iniciou = models.CharField(
        editable=False, default=Utils.obter_data_hora_atual, max_length=50
    )
    horario_fechamento = models.CharField(max_length=50, null=True, blank=True)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)

    class Meta:
        unique_together = (
            "pdv",
            "dia",
        )  # Garantir que não haja duplicatas de pdv e dia

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pdv.nome} - {self.dia}"


class AssociadoPDV(models.Model):
    id_associado = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    status_acesso = models.BooleanField(null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    pdv = models.ForeignKey(PDV, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)


class TransacaoPDV(models.Model):
    id_transacao = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    registro_diario = models.ForeignKey(
        RegistroDiarioPDV, on_delete=models.CASCADE, blank=True
    )
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=100)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)
