from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from .models import User, MovimentacaoSaldo, TokenIC, Grupo, Convite
from .serializers import TokenICSerializer, GrupoSerializer, AlunoSerializer, ConviteSerializer, \
    MovimentacaoSaldoSerializer, CadastroSerializer


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