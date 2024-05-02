# Generated by Django 5.0.4 on 2024-05-01 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_produto_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='associado',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='configuracao',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='galao',
            name='insert',
            field=models.DateTimeField(default='01/05/2024 16:39', editable=False),
        ),
        migrations.AlterField(
            model_name='gestaogalao',
            name='insert',
            field=models.DateTimeField(default='01/05/2024 16:39', editable=False),
        ),
        migrations.AlterField(
            model_name='historico',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='itemcompra',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='log',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='loja',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='motoboy',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='produto',
            name='insert',
            field=models.DateTimeField(default='01/05/2024 16:39', editable=False),
        ),
        migrations.AlterField(
            model_name='sessao',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='sessao',
            name='time_iniciou',
            field=models.DateTimeField(default='01/05/2024 16:39', null=True),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='venda',
            name='data_venda',
            field=models.CharField(default='01/05/2024', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='venda',
            name='insert',
            field=models.CharField(default='01/05/2024 16:39', editable=False, max_length=100),
        ),
    ]
