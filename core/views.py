from django.shortcuts import render
from perfis.models import Empresa, Freelancer, Freelancer
import vagas
from vagas.models import Candidatura, Vaga
from vagas.views import candidaturas
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

# Create your views here.
def homeFreelancer(request):
    vagas = Vaga.objects.all()
    return render(request, 'homeFreelancer.html', {
        'vagas': vagas
        })

def homeEmpresa(request):

    #empresa = request.user.empresa  # empresa logada
     # freelancer = Freelancer.objects.get(usuario=request.user)
    empresa = Empresa.objects.first()
    hoje = timezone.now().date()

    
    vagas = (
        Vaga.objects
        .filter(empresa=empresa)
    )
    
    for vaga in vagas:
        if vaga.status == 'aberto' and vaga.dataEvento < hoje:
            vaga.status = 'finalizado'
            vaga.save()

    abertos = vagas.filter( 
        status="aberto",
        dataEvento__gte=hoje
    )
    
    cancelados = vagas.filter(
        status="cancelado",
    )
    
    
    fechados = vagas.filter(
        status="fechado",
        dataEvento__gte=hoje
    )
    
    finalizadas = vagas.filter(
        Q(status="finalizado")|
        Q(status="aceito", dataEvento__lt=hoje)|
        Q(status = "fechado", dataEvento__lt = hoje)
    )
    vagasRestantes = vaga.quantidadeVagas - vaga.quantidadeSelecionados
    print("vagas finalizadas:", finalizadas)
    print("vagas abertas:", abertos)
    print("vagas canceladas:", cancelados)
    print("vagas fechadas:", fechados)
    
    
        
    context = {
        "vagas": vagas,

        "abertos": abertos,
        "cancelados": cancelados,
        "fechados": fechados,
        "finalizadas": finalizadas,
        "vagasRestantes" : vagasRestantes,

        "total_abertos": abertos.count(),
        "total_cancelados": cancelados.count(),
        "total_fechados": fechados.count(),
        "total_finalizadas": finalizadas.count(),
    }

    return render(request, "homeEmpresa.html", context)

