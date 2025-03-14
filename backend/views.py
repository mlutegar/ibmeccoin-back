from io import BytesIO

import qrcode
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout

from .models import User, Turma, MovimentacaoSaldo
from .serializers import UserLoginSerializer, SaldoAlunoSerializer, TokenICCreateSerializer, TokenICResponseSerializer


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


@extend_schema(request=UserLoginSerializer)
@api_view(["POST"])
def user_login_view(request):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "email": user.email,
            "tipo": user.tipo,
            "matricula": user.matricula,
        })

    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """Retorna nome, matrícula e tipo do usuário logado"""
    user = request.user

    return Response({
        "nome": user.get_full_name(),
        "email": user.email,
        "tipo": user.tipo,
        "matricula": user.matricula,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_saldo_aluno(request, matricula, turma_id):
    """Retorna o saldo do aluno em uma turma específica."""
    try:
        # Obtendo o aluno pelo número de matrícula
        aluno = User.objects.get(matricula=matricula, tipo='aluno')

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


@extend_schema(request=TokenICCreateSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_token_ic(request):
    serializer = TokenICCreateSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.save()
        response_serializer = TokenICResponseSerializer(token)
        return Response(response_serializer.data, status=201)
    return Response(serializer.errors, status=400)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="quantidade_ic",
            type=int,
            description="Número de ICs a serem gerados no Token",
            required=False,
            default=1
        )
    ],
    responses={200: "QR Code PNG"}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_qr(request):
    """
    Gera um QR Code contendo um Token IC.
    O parâmetro 'ic_count' define a quantidade de ICs no token.
    Exemplo: /api/generate_qr?ic_count=5
    """

    # Obtém a quantidade de ICs a partir do parâmetro da URL (padrão: 1)
    quantidade_ic = request.GET.get("quantidade_ic", 1)

    try:
        quantidade_ic = int(quantidade_ic)  # Converte para inteiro
        if quantidade_ic <= 0:
            return Response({"error": "quantidade_ic deve ser maior que zero."}, status=400)
    except ValueError:
        return Response({"error": "quantidade_ic deve ser um número inteiro válido."}, status=400)

    # Criar um novo Token IC com a quantidade de ICs especificada
    serializer = TokenICCreateSerializer(data={"quantidade_ic": quantidade_ic})

    if serializer.is_valid():
        token = serializer.save()
        response_serializer = TokenICResponseSerializer(token)
        token_ic = response_serializer.data.get("token")
        print(token_ic)

        # Gera o QR Code com o token gerado
        qr = qrcode.make(token_ic)

        # Salva a imagem em memória
        img_io = BytesIO()
        qr.save(img_io, format="PNG")
        img_io.seek(0)

        # Retorna a imagem do QR Code
        return HttpResponse(img_io, content_type="image/png")

    return Response(serializer.errors, status=400)
