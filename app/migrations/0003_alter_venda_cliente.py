# Generated by Django 5.0.2 on 2024-04-17 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_remove_cliente_id_cliente_id_cliente"),
    ]

    operations = [
        migrations.AlterField(
            model_name="venda",
            name="cliente",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="app.cliente"
            ),
        ),
    ]
