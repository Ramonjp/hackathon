from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

from doacao.models import Doacao
from .serializers import DoacaoSerializer, UserDoacoesListSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DoacaoCreateAPIView(generics.CreateAPIView):
    queryset = Doacao.objects.all()
    serializer_class = DoacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(pessoa=self.request.user)
        cpf = self.request.user.cpf
        valor = serializer.validated_data['valor']
        data = {
            'cpf': cpf,
            'app_name': 'marjo-helps',
            'valor': float(valor)
        }
        
        headers = {
            'api-key': 'HACKATON_UNIESP_MARJO_2024',
            'Content-Type': 'application/json'
        }

        url = 'https://hackathon.marjosports.com.br/hackathon'
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            response.raise_for_status()


class UserDoacoesListView(generics.ListAPIView):
    serializer_class = UserDoacoesListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Este view deve retornar uma lista de todas as doações
        para o usuário atualmente autenticado.
        """
        user = self.request.user
        return Doacao.objects.filter(pessoa=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        total_value = sum([doacao.valor for doacao in queryset])

        response_data = {
            'transacoes': data,
            'valorTotal': total_value
        }

        return Response(response_data)
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer