from django.db import models
from django.contrib.auth.models import AbstractUser
from usuario.models import Usuario


# Create your models here.

class Empresa(models.Model):  # modelo para representar as empresas que vão criar os eventos

    usuario = models.OneToOneField( #relacionamento um-para-um com o modelo Usuario, garantindo que cada empresa tenha um acesso associado
        Usuario,
        on_delete=models.CASCADE
    )
    
    nomeFantasia = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    descricao = models.TextField()
    site = models.URLField(blank=True, null=True) 
    telefone = models.CharField(max_length=20, blank=True, null=True)
    avaliacao_media = models.FloatField(default=0) 

    def __str__(self):  # método que retorna o nome fantasia da empresa quando for chamado
        return self.nomeFantasia


class Freelancer(models.Model): # modelo para representar os freelancers que vão se candidatar aos eventos
    
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE
    )

    AREAS = (  #alterar as áreas de atuação conforme necessário
        ('garcom', 'Garçom'),
        ('seguranca', 'Segurança'),
        ('barman', 'Barman'),
        ('fotografo', 'Fotógrafo'),
        ('outro', 'Outro'),
    )

    nomeCompleto = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    experiencia = models.TextField() #texto livre para o freelancer descrever sua experiência na área de atuação
    avaliacao_media = models.FloatField(default=0)
    area_atuacao = models.CharField(
        max_length=50,
        choices=AREAS
    )

    def __str__(self):
        return self.nomeCompleto

