# Generated by Django 5.1.7 on 2025-03-16 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_alter_movimentacaosaldo_data_movimentacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimentacaosaldo',
            name='descricao',
        ),
    ]
