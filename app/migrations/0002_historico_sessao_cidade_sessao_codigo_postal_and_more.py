# Generated by Django 5.0.2 on 2024-03-10 02:36

import app.models.usuario
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Historico",
            fields=[
                (
                    "id_historico",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("descricao", models.TextField(blank=True, null=True)),
                (
                    "insert",
                    models.DateTimeField(
                        db_column="date_time_insert", default=django.utils.timezone.now
                    ),
                ),
                (
                    "update",
                    models.DateTimeField(
                        db_column="date_time_update",
                        default=django.utils.timezone.now,
                        null=True,
                    ),
                ),
                (
                    "usuario",
                    models.UUIDField(
                        db_column="id", verbose_name=app.models.usuario.Usuario
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="sessao",
            name="cidade",
            field=models.CharField(
                blank=True, db_column="cidade", max_length=100, null=True
            ),
        ),
        migrations.AddField(
            model_name="sessao",
            name="codigo_postal",
            field=models.CharField(
                blank=True, db_column="codigo_postal", max_length=20, null=True
            ),
        ),
        migrations.AddField(
            model_name="sessao",
            name="latitude",
            field=models.DecimalField(
                blank=True,
                db_column="latitude",
                decimal_places=6,
                max_digits=9,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="sessao",
            name="longitude",
            field=models.DecimalField(
                blank=True,
                db_column="longitude",
                decimal_places=6,
                max_digits=9,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="sessao",
            name="organizacao",
            field=models.CharField(
                blank=True, db_column="organizacao", max_length=200, null=True
            ),
        ),
        migrations.AddField(
            model_name="sessao",
            name="pais",
            field=models.CharField(
                blank=True, db_column="pais", max_length=100, null=True
            ),
        ),
        migrations.AddField(
            model_name="sessao",
            name="regiao",
            field=models.CharField(
                blank=True, db_column="regiao", max_length=100, null=True
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="id",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name="loja",
            name="update",
            field=models.DateTimeField(
                db_column="date_time_update",
                default=django.utils.timezone.now,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="produto",
            name="update",
            field=models.DateTimeField(
                db_column="date_time_update",
                default=django.utils.timezone.now,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Log",
            fields=[
                (
                    "id_log",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("tipo", models.CharField(max_length=50)),
                ("origem", models.CharField(max_length=100)),
                ("descricao", models.TextField()),
                (
                    "insert",
                    models.DateTimeField(
                        db_column="date_time_insert", default=django.utils.timezone.now
                    ),
                ),
                (
                    "update",
                    models.DateTimeField(
                        db_column="date_time_update",
                        default=django.utils.timezone.now,
                        null=True,
                    ),
                ),
                ("ip_usuario", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "usuario",
                    models.ForeignKey(
                        db_column="id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app.usuario",
                    ),
                ),
            ],
        ),
    ]
