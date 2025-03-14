from django.contrib import admin
from .models import User, Turma, MovimentacaoSaldo, TokenIC


# Personalizando a exibição do modelo User no admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'tipo', 'matricula', 'first_name', 'last_name', 'email')  # Exibindo alguns campos no admin
    search_fields = ('username', 'first_name', 'last_name', 'email')  # Campos que podem ser pesquisados

# Registrando o modelo User com o UserAdmin
admin.site.register(User, UserAdmin)

# Personalizando a exibição do modelo Turma no admin
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'professor')  # Exibindo disciplina e professor
    search_fields = ('disciplina', 'professor__username')  # Permitindo pesquisa pela disciplina e pelo professor

# Registrando o modelo Turma com o TurmaAdmin
admin.site.register(Turma, TurmaAdmin)

# Personalizando a exibição do modelo MovimentacaoSaldo no admin
class MovimentacaoSaldoAdmin(admin.ModelAdmin):
    list_display = ('data_movimentacao', 'tipo', 'valor', 'aluno', 'turma')  # Exibindo detalhes da movimentação
    list_filter = ('tipo', 'turma')  # Filtros para tipo de movimentação e turma
    search_fields = ('aluno__username', 'turma__disciplina')  # Permitindo pesquisa pelos campos do aluno e turma

# Registrando o modelo MovimentacaoSaldo com o MovimentacaoSaldoAdmin
admin.site.register(MovimentacaoSaldo, MovimentacaoSaldoAdmin)
admin.site.register(TokenIC)