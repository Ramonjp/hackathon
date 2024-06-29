from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="API de Usuários",
        default_version='v1',
        description="API para criar usuários comuns",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourdomain.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('create-user/', views.UserCreateAPIView.as_view(), name='create-user'),
    path('doacoes/', views.DoacaoCreateAPIView.as_view(), name='doacao-create'),
    path('minhas-doacoes/', views.UserDoacoesListView.as_view(), name='user-doacoes-list'),
]