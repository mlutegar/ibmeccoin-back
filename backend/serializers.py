import uuid
from datetime import timedelta

from django.utils.timezone import now
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import User, MovimentacaoSaldo, TokenIC
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

class TokenICSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenIC
        fields = '__all__'
        extra_kwargs = {
            'quantidade_ic': {'required': True},
            'expiracao': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['expiracao'] = now() + timedelta(seconds=10)
        return super().create(validated_data)
