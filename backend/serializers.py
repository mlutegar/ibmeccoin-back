from datetime import timedelta
from django.utils.timezone import now
from rest_framework import serializers, viewsets
from .models import User, MovimentacaoSaldo, TokenIC, Grupo, Convite


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
        validated_data['expiracao'] = now() + timedelta(seconds=110)
        return super().create(validated_data)

class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Criptografa a senha
        user.save()
        return user

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'tipo']

class MovimentacaoSaldoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentacaoSaldo
        fields = '__all__'
        extra_kwargs = {
            'aluno': {'required': True},
            'turma': {'required': True},
            'valor': {'required': True},
            'tipo': {'required': True},
            'data_movimentacao': {'read_only': True}
        }

        def create(self, validated_data):
            validated_data['data_movimentacao'] = now()
            return super().create(validated_data)

class ConviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convite
        fields = '__all__'
        extra_kwargs = {
            'grupo': {'required': True},
            'destinatario': {'required': True},
            'remetente': {'required': True},
            'expiracao': {'read_only': True},
            'valido': {'read_only': True}
        }

        def create(self, validated_data):
            validated_data['expiracao'] = now() + timedelta(days=1)
            validated_data['valido'] = True
            return super().create(validated_data)

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'