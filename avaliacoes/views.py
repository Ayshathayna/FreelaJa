from django.shortcuts import render, redirect, get_object_or_404
from .models import AvaliaFreelancer, AvaliaVaga
from vagas.models import  Candidatura
from perfis.models import Freelancer, Empresa
from .forms import AvaliaVagaForm
from django.contrib import messages
from django.db.models import Avg


# Create your views here.


def avaliarVaga(request, candidatura_id):

    candidatura = get_object_or_404(
        Candidatura,
        id=candidatura_id
    )

    vaga = candidatura.vaga

    # freelancer = Freelancer.objects.get(usuario=request.user)
    freelancer = Freelancer.objects.first()  # teste

    if request.method == 'POST':

        form = AvaliaVagaForm(request.POST)  

        if form.is_valid():

            avaliacao = form.save(commit=False) 
            avaliacao.freelancer = freelancer
            avaliacao.vaga = vaga
            avaliacao.save()
            messages.success(request, "Avaliação salva com sucesso!")

            empresa = candidatura.vaga.empresa

            media = AvaliaVaga.objects.filter( # atualiza a média da empresa
                vaga__empresa=empresa
            ).aggregate(
                Avg('nota')
            )
            print(media)

            empresa.avaliacao_media = media['nota__avg'] or 0
            empresa.save()
            return redirect('verAvaliacao', candidatura_id=candidatura.id) # redireciona para ver a avaliação enviada

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
    
def verAvaliacao(request, candidatura_id):

    candidatura = get_object_or_404(
        Candidatura,
        id=candidatura_id
    )

    vaga = candidatura.vaga

    avaliacao = get_object_or_404(
        AvaliaVaga,
        freelancer=candidatura.freelancer,
        vaga=vaga
    )

    return render(
        request,
        'avaliarVaga.html',
         {
            'avaliacao': avaliacao,
            'vaga': vaga,
            'candidatura': candidatura, 
            'somente_leitura': True
         })
    
