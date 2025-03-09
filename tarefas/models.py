from datetime import timedelta

from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.IntegerField(primary_key=True, unique=True)
    senha = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.nome

class Tarefa(models.Model):
    """
    Modelo para Tarefa. Possui um nome, descrição, status, prioridade geral, prazo e data de criação e atualização
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    nome = models.CharField(max_length=255, verbose_name="Nome")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    grupo = models.CharField(max_length=255, blank=True, verbose_name="Grupo")
    prioridade = models.IntegerField(default=1, verbose_name="Prioridade")
    data_prazo = models.DateField(null=True, blank=True, verbose_name="Prazo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def get_nome(self):
        return self.nome

    def __str__(self):
        return self.nome


class Dia(models.Model):
    """
    Modelo para Dia
    """
    data = models.DateField(unique=True, verbose_name="Data")

    def __str__(self):
        return f"Dia {self.data}"


class TarefaDia(models.Model):
    """
    Modelo intermediário para associar Tarefa e Dia com prioridade
    """
    dia = models.ForeignKey(Dia, on_delete=models.CASCADE, related_name="tarefas_dia")
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name="dias_tarefa")
    prioridade = models.IntegerField(verbose_name="Prioridade", default=1)
    tempo_gasto = models.DurationField(
        null=True,
        blank=True,
        default=timedelta(seconds=0),
        verbose_name="Tempo gasto"
    )

    def aumentar_tempo_gasto(self):
        self.tempo_gasto += timedelta(minutes=15)
        self.save()

    class Meta:
        unique_together = ('dia', 'tarefa')  # Garante que a mesma tarefa não seja associada duas vezes ao mesmo dia

    def get_nome(self):
        return self.tarefa.get_nome()

    def get_prioridade(self):
        return self.prioridade

    def get_tempo_atual(self):
        """
        Retorna o tempo gasto em minutos
        :return: str
        """
        return self.tempo_gasto.total_seconds() // 60

    def __str__(self):
        return f"{self.tarefa.nome} em {self.dia.data} (Prioridade {self.prioridade}) - {self.tempo_gasto}"


class Situacao(models.Model):
    """
    Modelo para Situação do usuário, indíca em qual nível de concentração ele está:
        1 - Iniciando (música calma)
        2 - Explorando Ideias (música clássica)
        3 - Concentrado (música lo-fi)
        4 - Produtivo (música mbp)
        5 - Focado (músicas curtidas)
        6 - Ritmo Constante (músicas do dia)
        7 - Pico de produtividade (album a escolher)
        8 - Criativo (Músicas a escolher)
    """
    NIVEIS = [
        (1, 'Iniciando: Música Calma'),
        (2, 'Explorando Ideias: Música Clássica'),
        (3, 'Concentrado: Música Lo-fi'),
        (4, 'Produtivo: Música MBP'),
        (5, 'Focado: Músicas Curtidas'),
        (6, 'Ritmo Constante: Músicas do Dia'),
        (7, 'Pico de produtividade: Album a escolher'),
        (8, 'Criativo: Músicas a escolher'),
    ]

    usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='situacao')
    nivel = models.PositiveSmallIntegerField(default=1, verbose_name="Nível de concentração", choices=NIVEIS)

    def aumentar_nivel(self):
        if self.nivel < 9:  # Limite máximo
            self.nivel += 1
            self.save()

    def diminuir_nivel(self):
        if self.nivel > 1:  # Limite mínimo
            self.nivel -= 1
            self.save()

    def get_nome_nivel(self):
        return dict(self.NIVEIS)[self.nivel]

    def __str__(self):
        return f"{self.usuario.username} - Nível {self.nivel}"