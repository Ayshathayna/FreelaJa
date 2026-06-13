from django.shortcuts import render, get_object_or_404
from vagas.models import Candidatura, Vaga
from .models import Freelancer, Empresa
from avaliacoes.models import AvaliaFreelancer, AvaliaVaga


def perfilFreelancer(request, freelancer_id, candidatura_id):

    freelancer = get_object_or_404(
        Freelancer,
        id=freelancer_id
    )

    ultimas_vagas = (
        Candidatura.objects
        .filter(
            freelancer=freelancer,
            status="finalizado"
        )
        .select_related(
            "vaga",
            "vaga__empresa"
        )
        .order_by("-vaga__dataEvento")[:5]
    )
    candidatura = (
        Candidatura.objects
        .select_related("vaga", "vaga__empresa")
        .get(id=candidatura_id)
    )
    finalizado = candidatura.vaga.status == "finalizado"
    comentarios = (
        AvaliaFreelancer.objects
        .filter(
            freelancer=freelancer
        )
        .select_related(
            "vaga",
            "empresa"
        )
        .order_by("-id")
    )

    return render(
        request,
        "perfilFreelancer.html",
        {
            "freelancer": freelancer,
            "ultimas_vagas": ultimas_vagas,
            "comentarios": comentarios,
            "candidatura_id": candidatura_id,
            "finalizado":finalizado
        }
    )
    
    
def perfilEmpresa(request, empresa_id):

    empresa = get_object_or_404(
        Empresa,
        id=empresa_id
    )

    vagas = (
        Vaga.objects
        .filter(empresa=empresa)
        .order_by('-dataEvento')
    )

    ultimas_vagas = vagas[:5]

    avaliacoes = (
        AvaliaVaga.objects
        .filter(vaga__empresa=empresa)
        .select_related(
            'freelancer',
            'vaga'
        )
        .order_by('-criadoEm')
    )

    context = {

        'empresa': empresa,

        'ultimas_vagas': ultimas_vagas,

        'avaliacoes': avaliacoes,

        'total_vagas': vagas.count(),

        'total_avaliacoes': avaliacoes.count()

    }

    return render(
        request,
        'perfilEmpresa.html',
        context
    )