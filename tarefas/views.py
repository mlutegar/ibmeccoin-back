from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from tarefas.models import Tarefa, Situacao, Dia, TarefaDia


@login_required
def index(request):
    user = request.user

    situacao = Situacao.objects.get(id=user.id)
    tarefas = Tarefa.objects.all()

    # Manipula o aumento ou diminuição do nível
    if request.method == "POST" and 'aumentar' in request.POST:
        situacao.aumentar_nivel()
        return redirect('index')  # Redireciona para atualizar a página
    elif request.method == "POST" and 'diminuir' in request.POST:
        situacao.diminuir_nivel()
        return redirect('index')  # Redireciona para atualizar a página

    tarefas_do_dia = None

    hoje = datetime.today().strftime('%Y-%m-%d')
    if not Dia.objects.filter(data=hoje).exists():
        Dia.objects.create(data=hoje)
    else:
        # Verifica se há tarefas do dia de hoje, se não houver, redireciona para a página de tarefas
        if not Dia.objects.get(data=hoje).tarefas_dia.all().exists():
            return redirect('tarefas')
        else:
            tarefas_do_dia = Dia.objects.get(data=hoje).tarefas_dia.all().order_by('-prioridade')

    # Aumenta o tempo gasto na tarefa
    if request.method == "POST" and request.POST.get("acao") == "aumentar":
        tarefa_id = request.POST.get("tarefa_id")
        if tarefa_id:
            try:
                tarefa = TarefaDia.objects.get(id=tarefa_id)
                tarefa.tempo_gasto = (tarefa.tempo_gasto or timedelta()) + timedelta(
                    minutes=15)  # Incrementa 15 minutos
                tarefa.save()
            except Tarefa.DoesNotExist:
                pass  # Ignore se a tarefa não existir
        return redirect('index')  # Redireciona para evitar reenvio do formulário

    return render(request, 'index.html', {
        'tarefas': tarefas,
        'tarefas_do_dia': tarefas_do_dia,
        'situacao': situacao,
        'hoje': hoje,
    })


@login_required
def tarefas(request):
    tarefas_obj = Tarefa.objects.all()

    if request.method == "POST":
        if 'adicionar' in request.POST:
            nome = request.POST.get('nome')
            prioridade = request.POST.get('prioridade')
            tarefa = Tarefa.objects.create(nome=nome, prioridade=prioridade)
            tarefas_obj = Tarefa.objects.all()
            return render(request, 'tarefas.html', {
                'tarefas': tarefas_obj
            })

    return render(request, 'tarefas.html', {
        'tarefas': tarefas_obj
    })


@login_required
def criar_tarefa(request):
    """
    Função que cria uma nova tarefa no banco de dados
    :param request: Parâmetro que contém todas as informações da requisição feita pelo usuário
    :return: Retorna a página tarefas.html renderizada
    """
    if request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        prioridade = request.POST.get('importancia')
        Tarefa.objects.create(nome=nome, prioridade=prioridade, descricao=descricao)
        return redirect('tarefas')


@login_required
def adicionar_tarefa_ao_dia(request, tarefa_id):
    if request.method == "POST":
        hoje = datetime.today().strftime('%Y-%m-%d')
        tarefa = Tarefa.objects.get(id=tarefa_id)
        dia, created = Dia.objects.get_or_create(data=hoje)
        TarefaDia.objects.create(tarefa=tarefa, dia=dia)
        return redirect('tarefas')


def obter_info_tarefa(request):
    if request.method == "GET":
        tarefa_id = request.POST.get('tarefa_id')
        if not tarefa_id:
            return JsonResponse({'error': 'ID da tarefa não informado'}, status=400)

        try:
            tarefa = Tarefa.objects.get(id=tarefa_id)
            return JsonResponse({
                'nome': tarefa.nome,
                'descricao': tarefa.descricao,
                'prioridade': tarefa.prioridade,
                'grupo': tarefa.grupo.nome if tarefa.grupo else None
            })
        except Tarefa.DoesNotExist:
            return JsonResponse({'error': 'Tarefa não encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Erro inesperado: ' + str(e)}, status=500)
    return JsonResponse({'error': 'Método não permitido.'}, status=405)
