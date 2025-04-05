from django.db import IntegrityError
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, MovimentacaoSaldo, TokenIC, Grupo, Convite, TokenUso
from .serializers import TokenICSerializer, GrupoSerializer, AlunoSerializer, ConviteSerializer, \
    MovimentacaoSaldoSerializer, CadastroSerializer

class ProcessarToken(APIView):
    permission_classes = [AllowAny]  # Garante que o usuário esteja autenticado

    def post(self, request, token_id):
        turma_id = request.data.get("turma_id", 1)
        aluno_id = request.data.get("aluno_id")
        user = User.objects.get(id=aluno_id)
        try:
            token = TokenIC.objects.get(id=token_id)
        except TokenIC.DoesNotExist:
            return Response({"erro": "Token inválido ou não encontrado."},
                            status=status.HTTP_404_NOT_FOUND)

        # Tenta criar o registro de uso do token (garantido pelo unique_together em TokenUso)
        try:
            TokenUso.objects.create(aluno=user, label=token.label, token=token)
        except IntegrityError:
            return Response({"erro": "Token com esta label já foi utilizado por este aluno."},
                            status=status.HTTP_400_BAD_REQUEST)

        movimentacao = MovimentacaoSaldo.objects.create(
            valor=token.quantidade_ic,
            tipo="C",      # 'C' para crédito
            aluno=user,
            turma_id=turma_id
        )

        return Response({
            "sucesso": "Saldo creditado com sucesso!",
            "movimentacao": MovimentacaoSaldoSerializer(movimentacao).data
        }, status=status.HTTP_200_OK)


class TokenICViewSet(viewsets.ModelViewSet):
    queryset = TokenIC.objects.all()
    serializer_class = TokenICSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class MovimentacaoSaldoViewSet(viewsets.ModelViewSet):
    queryset = MovimentacaoSaldo.objects.all()
    serializer_class = MovimentacaoSaldoSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class CadastroView(generics.CreateAPIView):
    serializer_class = CadastroSerializer
    permission_classes = [AllowAny]  # Permite que qualquer pessoa se cadastre

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class ConviteViewSet(viewsets.ModelViewSet):
    queryset = Convite.objects.all()
    serializer_class = ConviteSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()