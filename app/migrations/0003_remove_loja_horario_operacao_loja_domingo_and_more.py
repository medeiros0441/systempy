# Generated by Django 5.0.2 on 2024-03-04 17:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_alter_cliente_endereco"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="loja",
            name="horario_operacao",
        ),
        migrations.AddField(
            model_name="loja",
            name="domingo",
            field=models.BooleanField(db_column="domingo", default=False),
        ),
        migrations.AddField(
            model_name="loja",
            name="horario_operacao_fim",
            field=models.TimeField(db_column="horario_operacao_fim", null=True),
        ),
        migrations.AddField(
            model_name="loja",
            name="horario_operacao_inicio",
            field=models.TimeField(db_column="horario_operacao_inicio", null=True),
        ),
        migrations.AddField(
            model_name="loja",
            name="quarta",
            field=models.BooleanField(db_column="quarta", default=False),
        ),
        migrations.AddField(
            model_name="loja",
            name="quinta",
            field=models.BooleanField(db_column="quinta", default=False),
        ),
        migrations.AddField(
            model_name="loja",
            name="sabado",
            field=models.BooleanField(db_column="sabado", default=False),
        ),
        migrations.AddField(
            model_name="loja",
            name="segunda",
            field=models.BooleanField(db_column="segunda", default=False),
        ),
        migrations.AddField(
            model_name="loja",
            name="sexta",
            field=models.BooleanField(db_column="sexta", default=False),
        ),
        migrations.AddField(
            model_name="loja",
            name="terca",
            field=models.BooleanField(db_column="terca", default=False),
        ),
    ]
