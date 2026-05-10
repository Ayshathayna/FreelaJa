from django.db import models
from perfis.models import Freelancer

# Create your models here.
  
class Disponibilidade(models.Model):

    DIAS_SEMANA = (
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    )

    freelancer = models.ForeignKey( #relacionamento muitos-para-um, onde um freelancer pode ter várias disponibilidades, mas cada disponibilidade pertence a um único freelancer
        Freelancer,
        on_delete=models.CASCADE,
        related_name='disponibilidades'
    )

    dia_semana = models.CharField(
        max_length=20,
        choices=DIAS_SEMANA
    )

    horarioInicio = models.TimeField()
    horarioFim = models.TimeField()
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.freelancer} - {self.dia_semana}"
