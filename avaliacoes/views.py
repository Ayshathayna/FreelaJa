from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import AvaliaFreelancer, AvaliaVaga
from .forms import AvaliaVagaForm, AvaliaFreelancerForm

from vagas.models import Candidatura
from perfis.models import Freelancer, Empresa

#************************************************* Freelancer **********************************************

@login_required
def avaliarVaga(request, candidatura_id):

    candidatura = get_object_or_404( # ao utilizar select related, vagaa, vaga__empresa e freelancer não faz outra consulta no banco
        Candidatura.objects.select_related(
            'vaga',
            'vaga__empresa',
            'freelancer'
        ),
        id=candidatura_id
    )

    freelancer = get_object_or_404(
        Freelancer,
        usuario=request.user
    )

    if candidatura.freelancer != freelancer:
        raise PermissionDenied()

    vaga = candidatura.vaga

    avaliacao_existente = AvaliaVaga.objects.filter(
        freelancer=freelancer,
        vaga=vaga
    ).first()

    if avaliacao_existente:
        return redirect(
            'verAvaliacao',
            candidatura_id=candidatura.id
        )

    if request.method == 'POST':

        form = AvaliaVagaForm(request.POST)

        if form.is_valid():

            avaliacao = form.save(commit=False)
            avaliacao.freelancer = freelancer
            avaliacao.vaga = vaga
            avaliacao.save()

            vaga.empresa.atualizar_media()
            

            messages.success(
                request,
                'Avaliação salva com sucesso!'
            )

            return redirect(
                'verAvaliacao',
                candidatura_id=candidatura.id
            )

    else:
        form = AvaliaVagaForm()

    return render(
        request,
        'avaliarVaga.html',
        {
            'form': form,
            'vaga': vaga,
            'candidatura': candidatura,
            'somente_leitura': False
        }
    )
#---------------------------------------------------------------------
@login_required
def verAvaliacao(request, candidatura_id):

    candidatura = get_object_or_404(
        Candidatura.objects.select_related(
            'vaga',
            'freelancer'
        ),
        id=candidatura_id
    )

    freelancer = get_object_or_404(
        Freelancer,
        usuario=request.user
    )

    if candidatura.freelancer != freelancer:
        raise PermissionDenied()

    avaliacao = get_object_or_404(
        AvaliaVaga,
        freelancer=freelancer,
        vaga=candidatura.vaga
    )

    return render(
        request,
        'avaliarVaga.html',
        {
            'avaliacao': avaliacao,
            'vaga': candidatura.vaga,
            'candidatura': candidatura,
            'somente_leitura': True
        }
    )


#************************************************* Empresa **********************************************

@login_required
def avaliarFreelancer(request, candidatura_id):

    candidatura = get_object_or_404(
        Candidatura.objects.select_related(
            'vaga',
            'vaga__empresa',
            'freelancer'
        ),
        id=candidatura_id
    )

    empresa = get_object_or_404(
        Empresa,
        usuario=request.user
    ) 
    vaga = candidatura.vaga

    if vaga.empresa != empresa:
        raise PermissionDenied()
    
    freelancer = candidatura.freelancer

    avaliacao_existente = AvaliaFreelancer.objects.filter(
        empresa=empresa,
        freelancer=freelancer,
        vaga=vaga
    ).first()

    if avaliacao_existente:

        return redirect(
            'verAvaliacaoFreelancer',
            candidatura_id=candidatura.id
        )

    if request.method == 'POST':

        form = AvaliaFreelancerForm(request.POST)

        if form.is_valid():

            avaliacao = form.save(commit=False)

            avaliacao.empresa = empresa
            avaliacao.freelancer = freelancer
            avaliacao.vaga = vaga

            avaliacao.save()

            freelancer.atualizar_media()

            messages.success(
                request,
                'Avaliação enviada com sucesso!'
            )

            return redirect(
                'verAvaliacaoFreelancer',
                candidatura_id=candidatura.id
            )

    else:
        form = AvaliaFreelancerForm()

    return render(
        request,
        'avaliarFreelancer.html',
        {
            'form': form,
            'freelancer': freelancer,
            'vaga': vaga,
            'somente_leitura': False
        }
    )
#---------------------------------------------------------------------

@login_required
def verAvaliacaoFreelancer(request, candidatura_id):

    candidatura = get_object_or_404(
        Candidatura.objects.select_related(
            'vaga',
            'vaga__empresa',
            'freelancer'
        ),
        id=candidatura_id
    )

    empresa = request.user.empresa

    if candidatura.vaga.empresa != empresa:
        raise PermissionDenied()

    avaliacao = get_object_or_404(
        AvaliaFreelancer,
        empresa=empresa,
        freelancer=candidatura.freelancer,
        vaga=candidatura.vaga
    )

    return render(
        request,
        'avaliarFreelancer.html',
        {
            'avaliacao': avaliacao,
            'freelancer': candidatura.freelancer,
            'vaga': candidatura.vaga,
            'somente_leitura': True
        }
    )
