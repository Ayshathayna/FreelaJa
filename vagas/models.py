from django.db import models
from perfis.models import Empresa, Freelancer
from django.core.exceptions import ValidationError

# Create your models here.

class Vaga(models.Model):
    
    imagem = models.ImageField(
        upload_to='vagas/static/img/', #diretório onde as imagens serão armazenadas
        blank=True,
        null=True
    )

    STATUS = (
        ('aberto', 'Aberto'), 
        ('cancelado', 'Cancelado'),
        ('fechado', 'Fechado'),
        ('finalizado', 'Finalizado'),
    )

    empresa = models.ForeignKey( # Uma empresa pode ter vários eventos, mas um evento pertence a apenas uma empresa
        Empresa,
        on_delete=models.CASCADE,
        related_name='vagas' 
        #related_name é usado para criar um nome de acesso reverso, permitindo acessar as vagas de uma empresa usando empresa.vagas
    )

    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    quantidadeVagas = models.IntegerField()
    quantidadeSelecionados = models.IntegerField(default=0)
    dataEvento = models.DateField()
    horarioInicio = models.TimeField() 
    horarioFim = models.TimeField()
    criadoEm = models.DateTimeField(auto_now_add=True)
    finalizadoEm = models.DateTimeField(blank=True, null=True)   
    endereco = models.CharField(max_length=255) 

    remuneracao = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='aberto'
    )

    def __str__(self):
        return self.titulo

class Candidatura(models.Model):

    STATUS = (
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
        ('finalizado', 'Finalizado'),
    )

    freelancer = models.ForeignKey( 
        Freelancer, #relacionamento muitos-para-um, onde um freelancer pode se candidatar a vários eventos, mas cada candidatura pertence a um único freelancer
        on_delete=models.CASCADE
    )

    vaga = models.ForeignKey(
        Vaga, #relacionamento muitos-para-um, onde uma vaga pode ter várias candidaturas, mas cada candidatura pertence a uma única vaga
        on_delete=models.CASCADE
    )

    data_candidatura = models.DateTimeField(auto_now_add=True)
        
    mensagem_risco = models.TextField(#campo para armazenar mensagem do risco de atraso
        blank=True,             #verificar se é valido deixar 
        null=True
    )

    confirmou_risco = models.BooleanField(default=False) #campo para o freelancer confirmar que leu e entendeu os riscos associados ao evento
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pendente'
    )

    class Meta:  #garante que um freelancer possa se candidatar uma vez para o mesmo evento
        unique_together = ('freelancer', 'vaga')
        
    def aceitar(self):

        vagas_ocupadas = self.vaga.quantidadeSelecionados

        if vagas_ocupadas >= self.vaga.quantidadeVagas:
            raise ValidationError("Limite de vagas atingido")
        
        self.status = 'aceito'
        self.save()
    
    def __str__(self):
        return f"{self.freelancer} - {self.vaga}"