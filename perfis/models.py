from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from usuario.models import Usuario
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


# Create your models here.

class Empresa(models.Model):  # modelo para representar as empresas que vão criar os eventos

    usuario = models.OneToOneField( #relacionamento um-para-um com o modelo Usuario, garantindo que cada empresa tenha um acesso associado
        Usuario,
        on_delete=models.CASCADE
    )
    foto = models.ImageField(
        upload_to='empresas/',
        blank=True,
        null=True
    )
    nomeFantasia = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    descricao = models.TextField()
    site = models.URLField(blank=True, null=True) 
    avaliacao_media = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):  # método que retorna o nome fantasia da empresa quando for chamado
        return self.nomeFantasia
    def atualizar_media(self):

        from avaliacoes.models import AvaliaEmpresa

        media = AvaliaEmpresa.objects.filter(
            vaga__empresa=self
        ).aggregate(
            Avg('nota')
        )

        self.avaliacao_media = media['nota__avg'] or 0
        self.save(update_fields=['avaliacao_media'])


class Freelancer(models.Model): # modelo para representar os freelancers que vão se candidatar aos eventos
    INTERESSES = [
        ("programacao", "Programação"),
        ("recepcao", "Recepção"),
        ("seguranca", "Segurança"),
        ("garcom", "Garçom"),
        ("bartender", "Bartender"),
        ("cozinha", "Cozinha / Buffet"),
        ("limpeza", "Limpeza"),
        ("som_luz", "Som e Luz"),
        ("montagem", "Montagem e Estrutura"),
        ("fotografia", "Fotografia"),
        ("filmagem", "Filmagem"),
        ("atendimento", "Atendimento"),
        ("geral", "Geral / Apoio"),
    ]
    
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE
    )
    foto = models.ImageField(
        upload_to='freelancers/',
        blank=True,
        null=True
    )
    nomeCompleto = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    dataNascimento = models.DateField(null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)
    experiencia = models.TextField() #texto livre para o freelancer descrever sua experiência na área de atuação
    avaliacao_media = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    interesses = models.JSONField(
        default=list,
        blank=True
    )

    def __str__(self):
        return self.nomeCompleto

    @property
    def idade(self):
        if not self.dataNascimento:
            return None
        hoje = date.today()
        return hoje.year - self.dataNascimento.year - (
            (hoje.month, hoje.day) < (self.dataNascimento.month, self.dataNascimento.day)
        )
    
    def atualizar_media(self):

        from avaliacoes.models import AvaliaFreelancer

        media = AvaliaFreelancer.objects.filter(
            freelancer=self
        ).aggregate(
            Avg('nota')
        )

        self.avaliacao_media = media['nota__avg'] or 0
        self.save(update_fields=['avaliacao_media'])

