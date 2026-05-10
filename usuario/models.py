from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Usuario(AbstractUser): #herda de AbstractUser para usar o sistema de autenticação do Django

    TIPOS = (
        ('empresa', 'Empresa'),
        ('freelancer', 'Freelancer'),
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPOS
    )
