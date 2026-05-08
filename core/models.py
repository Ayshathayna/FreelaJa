from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
# models.py

class Usuario(AbstractUser): #herda de AbstractUser para usar o sistema de autenticação do Django

    TIPOS = (
        ('empresa', 'Empresa'),
        ('freelancer', 'Freelancer'),
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPOS
    )

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


class Evento(models.Model):

    STATUS = (
        ('aberto', 'Aberto'), 
        ('cancelado', 'Cancelado'),
        ('fechado', 'Fechado'),
        ('finalizado', 'Finalizado'),
    )

    empresa = models.ForeignKey( # Uma empresa pode ter vários eventos, mas um evento pertence a apenas uma empresa
        Empresa,
        on_delete=models.CASCADE,
        related_name='eventos' 
        #related_name é usado para criar um nome de acesso reverso, permitindo acessar os eventos de uma empresa usando empresa.eventos
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
    remuneracao = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    endereco = models.CharField(max_length=255) 
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
    )

    freelancer = models.ForeignKey( 
        Freelancer,
        on_delete=models.CASCADE
    )

    evento = models.ForeignKey(
        Evento,
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
        unique_together = ('freelancer', 'evento')
        
    def aceitar(self):

        vagas_ocupadas = self.evento.quantidadeSelecionados

        if vagas_ocupadas >= self.evento.quantidadeVagas:
            raise ValidationError("Limite de vagas atingido")
        
        self.status = 'aceito'
        self.save()
    
    def __str__(self):
        return f"{self.freelancer} - {self.evento}"
    
    
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


#class Avaliacao(models.Model): 

#    evento = models.ForeignKey(
 #       Evento,
 #       on_delete=models.CASCADE,
 #       related_name='candidaturas'
 #   )

    # empresa = models.ForeignKey(
     #   Empresa,
      #  on_delete=models.CASCADE,
       # related_name='avaliacoes_recebidas'
    #)

  #  freelancer = models.ForeignKey( 
  #      Freelancer,
  #      on_delete=models.CASCADE,
   #     related_name='avaliacoes_recebidas'
   # )

  #  nota = models.IntegerField(
   #     validators=[MinValueValidator(0), MaxValueValidator(5)]
   # )

   # comentario = models.TextField()

   # criadoEm = models.DateTimeField(auto_now_add=True)

   # def __str__(self):
  #      return f"Avaliação {self.nota}"
    
    
    
#***************************************************************************************************************************
'''
verificar 


-adicionar endereço na empresa é valido?(visto que os eventos podem ter endereços distintos
-um evento poderá ter mais de uma empresa? como coop
-o horário de inicio de evento, será oq o frela terá que estar no local? ou realmente o inicio do evento
-verifica se vai ficar só o endereço ou se vai ter campos separados para rua, número, bairro, cidade, estado e CEP
-verificar se é valido deixar a mensagem de risco 
'''