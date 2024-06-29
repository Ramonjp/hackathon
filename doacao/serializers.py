from time import localtime
from rest_framework import serializers
from django.contrib.auth import get_user_model

from doacao.models import CustomUser, Doacao
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    cpf = serializers.CharField(max_length=14)  # Adicionando o campo CPF ao serializer

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'cpf']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class DoacaoSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = Doacao
        fields = ['id', 'pessoa', 'valor', 'descricao', 'formatted_date']

    def formatted_date(self, obj):
        if obj.data:
            return localtime(obj.data).strftime('%Y-%m-%d')

class UserDoacoesListSerializer(serializers.ModelSerializer):
    nome_usuario = serializers.SerializerMethodField()
    cpf_usuario = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = Doacao
        fields = ['id', 'pessoa', 'valor', 'data', 'nome_usuario', 'cpf_usuario', 'formatted_date', 'descricao']

    def get_nome_usuario(self, obj):
        if obj.pessoa:
            return obj.pessoa.username
        return None

    def get_cpf_usuario(self, obj):
        if hasattr(obj.pessoa, 'cpf'):
            return obj.pessoa.cpf
        return None
    
    def formatted_date(self, obj):
        if obj.data:
            return localtime(obj.data).strftime('%Y-%m-%d')
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Chame o método original para obter os tokens
        data['id'] = self.user.id  # Adicione o ID do usuário ao payload de resposta
        return data