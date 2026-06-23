from django.db import models
from perfis.models import Empresa, Freelancer
from django.utils import timezone

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
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    CATEGORIAS = [
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

    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIAS
    )

    detalhes = models.JSONField(
        default=list,
        blank=True
    )
    @property
    def vagasRestantes(self):
        return self.quantidadeVagas - self.quantidadeSelecionados
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

    def atualizar_status(self):

        agora = timezone.localtime()
        hoje = agora.date()

        # vaga já encerrada: passou a data, ou é hoje e o horário de término já passou
        evento_encerrado = (
            self.dataEvento < hoje
            or (self.dataEvento == hoje and self.horarioFim <= agora.time())
        )

        if self.status == 'cancelado':
            novo_status = self.status

        # qualquer vaga ativa (aberta ou lotada/fechada) vira finalizada ao encerrar
        elif self.status in ('aberto', 'fechado') and evento_encerrado:
            novo_status = 'finalizado'

        elif (
            self.status == 'aberto'
            and self.quantidadeSelecionados >= self.quantidadeVagas
        ):
            novo_status = 'fechado'

        elif (
            self.status == 'fechado'
            and self.quantidadeSelecionados < self.quantidadeVagas
            and not evento_encerrado
        ):
            novo_status = 'aberto'

        else:
            novo_status = self.status

        if novo_status != self.status:
            self.status = novo_status
            update_fields = ['status']

            if novo_status == 'finalizado' and not self.finalizadoEm:
                self.finalizadoEm = timezone.now()
                update_fields.append('finalizadoEm')

            self.save(update_fields=update_fields)
            
            
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

    def __str__(self):
        return f"{self.freelancer} - {self.vaga}"