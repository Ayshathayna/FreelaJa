from django.shortcuts import render, get_object_or_404
from perfis.models import Empresa, Freelancer
from vagas.models import Candidatura, Vaga
from django.utils import timezone
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required

#************************************************* Freelancer **********************************************

@login_required
def homeFreelancer(request):
    
    freelancer = get_object_or_404(
        Freelancer,
        usuario=request.user
    )
    vagas = Vaga.objects.filter(
        status='aberto'
    ).order_by('dataEvento')[:10]

    candidaturas_ids = set(
        Candidatura.objects.filter(
            freelancer=freelancer
        ).values_list(
            'vaga_id',
            flat=True
        )
    )
    for vaga in vagas:
        vaga.jaCandidatou = vaga.id in candidaturas_ids
        
    return render(request, 'homeFreelancer.html', {
        'vagas': vagas,
        'freelancer':freelancer
        })
    
#************************************************* Empresa **********************************************

@login_required
def homeEmpresa(request):

    empresa = get_object_or_404(
        Empresa,
        usuario=request.user
    )

    hoje = timezone.now().date()

    vagas = list(Vaga.objects.filter(
            empresa=empresa
        )
    )    
    for vaga in vagas:
        vaga.atualizar_status()
        
    vagas = Vaga.objects.filter(empresa=empresa)

    abertos = vagas.filter( 
        status="aberto",
        dataEvento__gte=hoje, 
        quantidadeVagas__gt=F('quantidadeSelecionados')
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
        Q(status="aberto", dataEvento__lt=hoje)|
        Q(status = "fechado", dataEvento__lt = hoje)
    )
        
    context = {
        "vagas": vagas,

        "abertos": abertos,
        "cancelados": cancelados,
        "fechados": fechados,
        "finalizadas": finalizadas,

        "total_abertos": abertos.count(),
        "total_cancelados": cancelados.count(),
        "total_fechados": fechados.count(),
        "total_finalizadas": finalizadas.count(),
    }

    return render(request, "homeEmpresa.html", context)

