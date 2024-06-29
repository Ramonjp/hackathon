from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime

class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=11)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_set',
        help_text=_('Specific permissions for this user.'),
    )

    def __str__(self):
        return self.username

class Doacao(models.Model):
    pessoa = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='doacoes')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Doação de {self.valor}'
    
    def formatted_date(self):
        # Este método retorna a data formatada ou o username se a data existir
        if self.data:
            return localtime(self.data).strftime('%Y-%m-%d')