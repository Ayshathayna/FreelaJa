
from django.db import models
from usuario.models import Usuario


class Notificacao(models.Model):

    TIPOS = [
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
        ('cancelada', 'Vaga Cancelada'),
        ('finalizada', 'Vaga Finalizada'),
        ('editada', 'Vaga Editada'),
        ('avaliacao', 'Avaliação'),
        ('sistema', 'Sistema'),
        ('candidatura', 'Nova candidatura'),

    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )

    titulo = models.CharField(max_length=100)

    mensagem = models.TextField()

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    link = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    lida = models.BooleanField(
        default=False
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-data_criacao']