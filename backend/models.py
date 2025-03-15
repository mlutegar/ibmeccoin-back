from datetime import timedelta

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):  # Agora usamos AbstractUser, herdando todas as funcionalidades do Django
    TIPO_CHOICES = (
        ("aluno", "Aluno"),
        ("professor", "Professor"),
        ("admin", "Administrador"),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="aluno")

    def __str__(self):
        return f"{self.username} - {self.tipo}"


class Turma(models.Model):
    disciplina = models.CharField(max_length=50)
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'professor'},
        related_name='turmas_professor'  # Nome exclusivo para acesso reverso
    )
    alunos = models.ManyToManyField(
        User,
        limit_choices_to={'tipo': 'aluno'},
        related_name='turmas_aluno'  # Nome exclusivo para acesso reverso
    )

    def __str__(self):
        alunos_nomes = ", ".join(self.alunos.values_list("username", flat=True))
        return f"{self.disciplina} - Alunos: {alunos_nomes}" if alunos_nomes else self.disciplina


class TokenIC(models.Model):
    quantidade_ic = models.IntegerField()
    expiracao = models.DateTimeField()

    def __str__(self):
        return f"Token de {self.quantidade_ic} expira em {self.expiracao}"

    def expirado(self):
        return now() > self.expiracao


class MovimentacaoSaldo(models.Model):
    TIPOS_MOVIMENTACAO = [
        ("C", "Crédito"),
        ("D", "Débito"),
    ]

    data_movimentacao = models.DateField(auto_now_add=True)
    valor = models.IntegerField()
    tipo = models.CharField(max_length=1, choices=TIPOS_MOVIMENTACAO)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movimentacoes", limit_choices_to={'tipo': 'aluno'})  # Relacionamento com Aluno
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    descricao = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.tipo} - {self.valor} ({self.aluno.username})"  # Exibe o username do aluno
