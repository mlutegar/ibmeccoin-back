from django.contrib import admin
from .models import Tarefa, Dia, TarefaDia, Situacao


class TaskAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo', 'data_prazo', 'created_at', 'updated_at')
    list_filter = ('grupo', 'data_prazo', 'created_at')
    search_fields = ('nome', 'descricao')
    ordering = ('data_prazo',)
    date_hierarchy = 'data_prazo'


class TarefaInline(admin.TabularInline):
    model = TarefaDia
    extra = 1  # Quantidade de linhas extras para adicionar novas tarefas
    fields = ('tarefa', 'prioridade', 'tempo_gasto')  # Exibe apenas os campos necessários
    ordering = ('-prioridade',)  # Ordena as tarefas por prioridade em ordem decrescente


class DiaAdmin(admin.ModelAdmin):
    list_display = ('data',)
    inlines = [TarefaInline]  # Permite editar as tarefas e prioridades diretamente no admin de Dia


admin.site.register(Tarefa, TaskAdmin)
admin.site.register(Dia, DiaAdmin)
admin.site.register(TarefaDia)
admin.site.register(Situacao)
