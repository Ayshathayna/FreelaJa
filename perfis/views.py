from django.shortcuts import render, get_object_or_404
from vagas.models import Candidatura
from .models import Freelancer
from avaliacoes.models import AvaliaFreelancer


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
            "candidatura_id": candidatura_id
        }
    )