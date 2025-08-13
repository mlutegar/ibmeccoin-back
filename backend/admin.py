from django.contrib import admin
from .models import User, Turma, MovimentacaoSaldo, TokenIC, Grupo, Convite, TokenUso, ProdutoLoja


# Personalizando a exibição do modelo User no admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'tipo', 'first_name', 'last_name', 'email')  # Exibindo alguns campos no admin
    search_fields = ('username', 'first_name', 'last_name', 'email')  # Campos que podem ser pesquisados

# Registrando o modelo User com o UserAdmin
admin.site.register(User, UserAdmin)

# Personalizando a exibição do modelo Turma no admin
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'professor')  # Exibindo disciplina e professor
    search_fields = ('disciplina', 'professor__username')  # Permitindo pesquisa pela disciplina e pelo professor

# Registrando o modelo Turma com o TurmaAdmin
admin.site.register(Turma, TurmaAdmin)


class MovimentacaoSaldoAdmin(admin.ModelAdmin):
    list_display = (
    'data_movimentacao', 'tipo', 'valor', 'get_nome_aluno', 'turma')  # Trocamos 'aluno' por 'get_nome_aluno'
    list_filter = ('data_movimentacao', 'tipo', 'turma')  # Adicionamos filtro por data_movimentacao
    search_fields = ('aluno__username', 'aluno__first_name', 'aluno__last_name',
                     'turma__disciplina')  # Adicionamos campos para pesquisa por nome

    def get_nome_aluno(self, obj):
        # Verifica se o aluno tem nome completo cadastrado
        if obj.aluno.first_name and obj.aluno.last_name:
            return f"{obj.aluno.first_name} {obj.aluno.last_name}"
        # Se não tiver nome completo, usa o nome de usuário
        return obj.aluno.username

    # Define o nome da coluna no admin
    get_nome_aluno.short_description = 'Aluno'
    # Permite ordenação pela coluna
    get_nome_aluno.admin_order_field = 'aluno__username'


admin.site.register(MovimentacaoSaldo, MovimentacaoSaldoAdmin)
admin.site.register(TokenIC)
admin.site.register(Grupo)
admin.site.register(Convite)
admin.site.register(TokenUso)
admin.site.register(ProdutoLoja)
