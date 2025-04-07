from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, MovimentacaoSaldo, TokenIC, Grupo, Convite, TokenUso
from .serializers import TokenICSerializer, GrupoSerializer, AlunoSerializer, ConviteSerializer, \
    MovimentacaoSaldoSerializer, CadastroSerializer


class ProcessarToken(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['token_id', 'aluno_id'],
            properties={
                'token_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID do token'),
                'aluno_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID do aluno'),
                'turma_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID da turma', default=1),
            }
        ),
        responses={
            200: openapi.Response('Sucesso', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'sucesso': openapi.Schema(type=openapi.TYPE_STRING),
                    'movimentacao': openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )),
            400: 'Erro de requisição inválida',
            404: 'Token ou usuário não encontrado',
        },
        operation_description="Processa um token, creditando o valor ao aluno especificado"
    )

    def post(self, request):  # Remove token_id parameter
        token_id = request.data.get("token_id")  # Get token_id from request body
        turma_id = request.data.get("turma_id", 1)
        aluno_id = request.data.get("aluno_id")

        # Validate token_id is provided
        if not token_id:
            return Response({"erro": "token_id é obrigatório"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=aluno_id)
        except User.DoesNotExist:
            return Response({"erro": "Usuário não encontrado"},
                            status=status.HTTP_404_NOT_FOUND)

        token = TokenIC.objects.filter(id=token_id).first()

        if not token:
            return Response({"erro": "Token não encontrado"},
                            status=status.HTTP_404_NOT_FOUND)

        if token.expirado():
            return Response({"erro": "Token expirado"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verifica se já existe um registro de uso para este aluno e a label do token
            token_ja_usado = TokenUso.objects.filter(aluno=user, label=token.label).exists()

            if token_ja_usado:
                return Response({"erro": "Este aluno já utilizou um token com esta label"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Se não foi usado, registre o uso
            TokenUso.objects.create(
                aluno=user,
                token=token,
                label=token.label
            )

        except Exception as e:
            return Response({"erro": f"Erro ao verificar uso do token: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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