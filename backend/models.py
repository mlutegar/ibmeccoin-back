from django.contrib.auth.models import AbstractUser
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


class Grupo(models.Model):
    nome = models.CharField(max_length=50)
    limite_aluno = models.IntegerField()
    turma = models.ForeignKey("Turma", on_delete=models.CASCADE)
    alunos = models.ManyToManyField("User", blank=True)
    saldo = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Convite(models.Model):
    valido = models.BooleanField(default=True)
    expiracao = models.DateTimeField(blank=True, null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name='convites_recebidos', on_delete=models.CASCADE)
    remetente = models.ForeignKey(User, related_name='convites_enviados', on_delete=models.CASCADE)

    def __str__(self):
        return f"Convite para {self.destinatario.username} do grupo {self.grupo.nome}"

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
    label = models.CharField(max_length=50)  # Novo campo para a label

    def __str__(self):
        return f"Token de {self.quantidade_ic} para '{self.label}' expira em {self.expiracao}"

    def expirado(self):
        return now() > self.expiracao

class TokenUso(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=50, default="")
    token = models.ForeignKey(TokenIC, on_delete=models.CASCADE)
    usado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("aluno", "label")  # Garante uso único da label por aluno

    def __str__(self):
        return f"{self.aluno.username} usou token com label '{self.label}' em {self.usado_em}"

class MovimentacaoSaldo(models.Model):
    TIPOS_MOVIMENTACAO = [
        ("C", "Crédito"),
        ("D", "Débito"),
    ]

    data_movimentacao = models.DateTimeField(auto_now_add=True)
    valor = models.IntegerField()
    tipo = models.CharField(max_length=1, choices=TIPOS_MOVIMENTACAO)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movimentacoes", limit_choices_to={'tipo': 'aluno'})  # Relacionamento com Aluno
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.valor} ({self.aluno.username})"  # Exibe o username do aluno
