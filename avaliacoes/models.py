from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from perfis.models import Freelancer, Empresa
from vagas.models import Vaga


class AvaliaEmpresa(models.Model):

    freelancer = models.ForeignKey( #relacionamento muitos-para-um, onde um freelancer pode avaliar várias empresas, mas cada avaliação pertence a um único freelancer
        Freelancer,
        on_delete=models.CASCADE
    )

    vaga = models.ForeignKey( # a vaga identifica a empresa avaliada (vaga.empresa) e o evento de origem da avaliação
        Vaga,
        on_delete=models.CASCADE
    )

    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comentario = models.TextField(blank=True)
    criadoEm = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('freelancer', 'vaga')

    def __str__(self):
        return f"{self.freelancer} avaliou {self.vaga.empresa}"
    #método para exibir o freelancer e a empresa avaliada

class AvaliaFreelancer(models.Model):

    empresa = models.ForeignKey( #relacionamento muitos-para-um, onde uma empresa pode avaliar vários freelancers, mas cada avaliação pertence a uma única empresa
        Empresa,
        on_delete=models.CASCADE
    )

    freelancer = models.ForeignKey( #relacionamento muitos-para-um, onde um freelancer pode ser avaliado por várias empresas, mas cada avaliação pertence a um único freelancer
        Freelancer,
        on_delete=models.CASCADE
    )
    vaga = models.ForeignKey(#
        Vaga,
        on_delete=models.CASCADE
)
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comentario = models.TextField(blank=True)
    criadoEm = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('empresa', 'freelancer', 'vaga') #garante que uma empresa possa avaliar um freelancer apenas uma vez por vaga
    def __str__(self):
        return f"{self.empresa} avaliou {self.freelancer}"
    