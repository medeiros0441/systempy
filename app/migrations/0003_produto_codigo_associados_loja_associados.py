# Generated by Django 5.0.2 on 2024-03-17 14:52

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_produto_codigo_configuracao"),
    ]

    operations = [
        
        migrations.CreateModel(
            name="Associados",
            fields=[
                (
                    "id_associado",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("insert", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "update",
                    models.DateTimeField(default=django.utils.timezone.now, null=True),
                ),
                ("status_acesso", models.BooleanField(default=True)),
                (
                    "usuario",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.usuario",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="loja",
            name="associados",
            field=models.ManyToManyField(to="app.associados"),
        ),
    ]
