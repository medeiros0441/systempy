# Generated by Django 5.0.4 on 2024-06-24 16:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0011_transacaopdv_usuario_alter_pdv_status_operacao_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="transacaopdv",
            name="tipo_operacao",
            field=models.IntegerField(
                blank=True, choices=[(1, "Entrou"), (2, "Retirado")], null=True
            ),
        ),
    ]
