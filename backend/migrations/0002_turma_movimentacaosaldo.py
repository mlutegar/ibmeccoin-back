# Generated by Django 5.1.7 on 2025-03-10 23:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disciplina', models.CharField(max_length=50)),
                ('alunos', models.ManyToManyField(limit_choices_to={'tipo': 'aluno'}, related_name='turmas_aluno', to=settings.AUTH_USER_MODEL)),
                ('professor', models.ForeignKey(limit_choices_to={'tipo': 'professor'}, on_delete=django.db.models.deletion.CASCADE, related_name='turmas_professor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovimentacaoSaldo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_movimentacao', models.DateField(auto_now_add=True)),
                ('valor', models.IntegerField()),
                ('tipo', models.CharField(choices=[('C', 'Crédito'), ('D', 'Débito')], max_length=1)),
                ('descricao', models.TextField(max_length=255)),
                ('aluno', models.ForeignKey(limit_choices_to={'tipo': 'aluno'}, on_delete=django.db.models.deletion.CASCADE, related_name='movimentacoes', to=settings.AUTH_USER_MODEL)),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.turma')),
            ],
        ),
    ]
