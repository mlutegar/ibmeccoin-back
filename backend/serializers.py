import uuid
from datetime import timedelta

from django.utils.timezone import now
from rest_framework import serializers
from .models import User, MovimentacaoSaldo, TokenIC
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        senha = data.get("senha")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado.")

        if not user.check_password(senha):  # Agora usa hashing de senha corretamente
            raise serializers.ValidationError("Senha incorreta.")

        data["user"] = user
        return data


class AlunoTokenObtainSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, aluno):
        token = super().get_token(aluno)

        # Adiciona informações personalizadas ao token
        token["aluno_id"] = aluno.matricula
        token["email"] = aluno.email

        return token


class AlunoTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, aluno):
        token = super().get_token(aluno)

        # Adiciona o aluno_id e email no token JWT
        token["aluno_id"] = aluno.matricula
        token["email"] = aluno.email

        return token


class SaldoAlunoSerializer(serializers.Serializer):
    aluno = serializers.CharField()
    turma = serializers.CharField()
    saldo = serializers.IntegerField()

    def to_representation(self, instance):
        aluno = instance['aluno']
        turma = instance['turma']
        saldo = instance['saldo']

        return {
            'aluno': aluno,
            'turma': turma,
            'saldo': saldo
        }

class TokenICCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenIC
        fields = ['quantidade_ic']  # Exige apenas a quantidade_ic no input

    def create(self, validated_data):
        token_valor = str(uuid.uuid4())  # Gera um valor único para o token
        quantidade_ic = validated_data.get('quantidade_ic')
        token = TokenIC.objects.create(
            valor=token_valor,
            quantidade_ic=quantidade_ic,
            expiracao=now() + timedelta(seconds=10)  # Define a expiração para 10 segundos
        )
        return token

class TokenICResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenIC
        fields = ['valor', 'quantidade_ic', 'expiracao']