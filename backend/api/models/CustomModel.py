from django.db import models
from django.utils import timezone
import datetime

      


class CustomModel(models.Model, metaclass=models.base.ModelBase):
    _insert = models.DateTimeField(auto_now_add=True, editable=False)
    _update = models.DateTimeField(auto_now=True)

    @property
    def update(self):
        """
        Retorna a data de atualização formatada no padrão brasileiro.
        """
        return self._update.strftime("%d/%m/%Y %H:%M")

    @update.setter
    def update(self, value):
        """
        Define a data de atualização com um valor datetime. 
        """
        if isinstance(value, datetime.datetime):
            self._update = value
        else:
            raise ValueError("O valor deve ser uma instância de datetime")

    def save(self, *args, **kwargs):
        # Atualiza o campo '_update' com a data e hora atuais antes de salvar
        self._update = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True