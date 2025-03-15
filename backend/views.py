from io import BytesIO

import qrcode
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout

from .models import User, Turma, MovimentacaoSaldo, TokenIC
from .serializers import SaldoAlunoSerializer, TokenICSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user if hasattr(self, "user") else request.user
        response.data.update({"user_id": user.id, "email": user.email})
        return response


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout realizado com sucesso."})





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """Retorna nome, matrícula e tipo do usuário logado"""
    user = request.user

    return Response({
        "nome": user.get_full_name(),
        "email": user.email,
        "tipo": user.tipo,
        "matricula": user.username,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_saldo_aluno(request, matricula, turma_id):
    """Retorna o saldo do aluno em uma turma específica."""
    try:
        # Obtendo o aluno pelo número de matrícula
        aluno = User.objects.get(username=matricula, tipo='aluno')

        # Obtendo a turma pelo ID
        turma = Turma.objects.get(id=turma_id)

        # Verificando se o aluno está matriculado na turma
        if aluno not in turma.alunos.all():
            return Response({"detail": "Aluno não está matriculado nesta turma."}, status=400)

        # Calculando o saldo do aluno na turma
        movimentacoes = MovimentacaoSaldo.objects.filter(aluno=aluno, turma=turma)
        saldo = sum(
            [movimentacao.valor if movimentacao.tipo == 'C' else -movimentacao.valor for movimentacao in movimentacoes])

        # Preparando os dados para resposta
        data = {
            'aluno': aluno.username,
            'turma': turma.disciplina,
            'saldo': saldo
        }

        # Retornando a resposta com os dados do saldo
        return Response(SaldoAlunoSerializer(data).data)

    except User.DoesNotExist:
        return Response({"detail": "Aluno não encontrado."}, status=404)
    except Turma.DoesNotExist:
        return Response({"detail": "Turma não encontrada."}, status=404)


class TokenICViewSet(viewsets.ModelViewSet):
    queryset = TokenIC.objects.all()
    serializer_class = TokenICSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
