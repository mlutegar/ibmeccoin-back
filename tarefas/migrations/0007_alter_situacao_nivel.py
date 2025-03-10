# Generated by Django 5.1.4 on 2024-12-18 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0006_situacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situacao',
            name='nivel',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Iniciando: Música Calma'), (2, 'Explorando Ideias: Música Clássica'), (3, 'Concentrado: Música Lo-fi'), (4, 'Produtivo: Música MBP'), (5, 'Focado: Músicas Curtidas'), (6, 'Ritmo Constante: Músicas do Dia'), (7, 'Pico de produtividade: Album a escolher'), (8, 'Criativo: Músicas a escolher')], default=1, verbose_name='Nível de concentração'),
        ),
    ]
