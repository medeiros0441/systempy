# Generated by Django 5.0.4 on 2024-05-13 19:30

import app.utils
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="associado",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="associado",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="caixa",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="caixa",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="configuracao",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="configuracao",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="empresa",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="empresa",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="endereco",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="endereco",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="entrega",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="entrega",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="galao",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="galao",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="gestaogalao",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="gestaogalao",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="historico",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="historico",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="itemcompra",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="itemcompra",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="log",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="log",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="loja",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="loja",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="motoboy",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="motoboy",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="produto",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="produto",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="sessao",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="sessao",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="transacao",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="transacao",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="venda",
            name="insert",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual,
                editable=False,
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="venda",
            name="update",
            field=models.CharField(
                default=app.utils.utils.obter_data_hora_atual, max_length=100
            ),
        ),
    ]
