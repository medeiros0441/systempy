# Generated by Django 5.0.2 on 2024-03-12 17:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_sessao_id_alter_sessao_descricao_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sessao",
            name="latitude",
        ),
        migrations.RemoveField(
            model_name="sessao",
            name="longitude",
        ),
    ]
