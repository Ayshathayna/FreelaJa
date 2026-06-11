from django.shortcuts import render, redirect, get_object_or_404
from avaliacoes.models import AvaliaVaga
from perfis.models import  Empresa, Freelancer
from .models import Vaga,  Candidatura
from .forms import VagaForm
from datetime import date
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q


#--------------------------------------------------------- EMPRESA --------------------------------------------------------------------
def criarVaga(request):

    if request.method == 'POST': #verifica se o método da requisição é POST, ou seja, se o formulário foi submetido. Se for, ele processa os dados do formulário.

        form = VagaForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():  #verifica se os dados do formulário são válidos. Se forem, ele salva a vaga no banco de dados.

            vaga = form.save(commit=False) #form.save(commit=False) salva os dados do formulário, mas não os envia para o banco de dados ainda. Isso permite que você faça modificações adicionais na instância do modelo antes de salvá-la.

            # empresa = Empresa.objects.get( #recupera a empresa associada ao usuário logado. Ele usa o método get() para buscar a empresa com base no usuário atual (request.user).
            #     usuario=request.user
            # )
            empresa = Empresa.objects.get(
                nomeFantasia="empresa"
            )
            vaga.empresa = empresa

            vaga.save()  #salva a vaga no banco de dados.
            messages.success(request, "Vaga criada com sucesso!")

            return redirect(
                'homeEmpresa'
            )
        else:
            print(form.errors) #se o formulário não for válido, ele imprime os erros no console
    else:
        form = VagaForm() 

    return render(
        request,
        'criarEditarVaga.html',
        {
            'form': form
        }
    )


def editarVaga(request,id):

    vaga = get_object_or_404(Vaga,id=id)

    if request.method == "POST":

        form = VagaForm(
            request.POST,
            request.FILES,
            instance=vaga
        )

        if form.is_valid():

            form.save()
            messages.success(request, "Vaga editada com sucesso!")

            return redirect(
                "homeEmpresa"
            )

    else:   
        form = VagaForm(instance=vaga)
    return render(
        request,
        "criarEditarVaga.html",
        {
            "form": form,
            "editar": True,
            "vaga": vaga
        }
    )

def excluirVaga(request, id):

    vaga = get_object_or_404(
        Vaga,
        id=id
    )

    vaga.delete()
    messages.success(request, "Vaga deletada com sucesso!")

    return redirect(
        "homeEmpresa"
    )

def candidatosVaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    hoje = timezone.now().date()

    candidaturas = Candidatura.objects.filter(
        vaga=vaga
    ).select_related('freelancer', 'freelancer__usuario')
    
    vagasRestantes = vaga.quantidadeVagas - vaga.quantidadeSelecionados

    pendentes = candidaturas.filter( 
        status="pendente",
        vaga__dataEvento__gte=hoje
    )
    
    recusadas = candidaturas.filter(
        Q(status="recusado") |
        Q(status="pendente", vaga__dataEvento__lt=hoje)
    )
    
    aceitas = candidaturas.filter(status="aceito")
    
    context = {
        "vaga": vaga,
        "candidaturas": candidaturas,

        "pendentes": pendentes,
        "aceitas": aceitas,
        "recusadas": recusadas,

        "total_analise": pendentes.filter(vaga__dataEvento__gte=hoje).count(),
        "total_aceitas": aceitas.filter( vaga__dataEvento__gte=hoje).count(),
        "total_recusadas": recusadas.count(),
        "vagas_restantes": vagasRestantes

    }

    return render(request, 'candidatos.html', context)

def aceitarCandidatura(request, id):
    candidatura = get_object_or_404(Candidatura, id=id)
    
    if(candidatura.vaga.quantidadeVagas <= candidatura.vaga.quantidadeSelecionados):
        messages.error(request, "Não há vagas disponíveis para aceitar mais candidatos.")
        return redirect('candidatosVaga', vaga_id=candidatura.vaga.id)
    
    candidatura.status = "aceito"
    candidatura.vaga.quantidadeSelecionados += 1
    
    candidatura.vaga.save()
    candidatura.save()
    
    messages.success(request, "Candidato aceito com sucesso!")
    return redirect('candidatosVaga', vaga_id=candidatura.vaga.id)

def recusarCandidatura(request, id):
    candidatura = get_object_or_404(Candidatura, id=id)
    candidatura.status = "recusado"
    candidatura.vaga.quantidadeSelecionados -= 1
    candidatura.vaga.save()
    candidatura.save()

    messages.warning(request, "Candidato recusado.")
    return redirect('candidatosVaga', vaga_id=candidatura.vaga.id)



def finalizarVaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    vaga.status = "finalizado"
    vaga.save()
    
    for candidatura in vaga.candidaturas.filter(status="aceito"):
        candidatura.status = "finalizado"
        candidatura.save()
        
    for candidatura in vaga.candidaturas.filter(status="pendente"):
        candidatura.status = "recusado"
        candidatura.save()

    messages.success(request, "Vaga finalizada com sucesso!")
    return redirect('homeEmpresa')
#--------------------------------------------------------- FREELANCER --------------------------------------------------------------------

def verVaga(request, id):   
    vaga = get_object_or_404(Vaga, id=id)

    return render(request, "verVaga.html", {
        "vaga": vaga
    })


def candidatarVaga(request, vaga_id):
    url_anterior = request.META.get('HTTP_REFERER')

    vaga = get_object_or_404(Vaga, id=vaga_id)

    #freelancer = Freelancer.objects.get(usuario=request.user)  -> o correto
    freelancer = Freelancer.objects.first()  # pega o primeiro do banco, apenas para teste

    qs = Candidatura.objects.filter( #verifica se o freelancer já se candidatou para a vaga
        vaga=vaga,
        freelancer=freelancer
    )

    if qs.exists():
        messages.warning(request, "Você já se candidatou para esta vaga.")
        if url_anterior:
            return redirect(url_anterior)

        return redirect("verVaga", id=vaga.id)

    Candidatura.objects.create(
        vaga=vaga,
        freelancer=freelancer
    )
 
    messages.success(request, "Candidatura enviada com sucesso!")

    if url_anterior:
        return redirect(url_anterior)

    return redirect('verVaga', id=vaga.id)


def listarVagas(request):
    query = request.GET.get('q', '').strip()
    vagas = Vaga.objects.filter(status='aberto')

    if query:
        vagas = vagas.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query) |
            Q(endereco__icontains=query)
        )

    return render(request, 'vagas.html', {
        'vagas': vagas,
        'query': query
    })

def candidaturas(request):
    # freelancer = Freelancer.objects.get(usuario=request.user)
    freelancer = Freelancer.objects.first()  # teste

    hoje = timezone.now().date()

    candidaturas = (
        Candidatura.objects
        .filter(freelancer=freelancer)
        .select_related("vaga", "vaga__empresa")
    )

    pendentes = candidaturas.filter( 
        status="pendente",
        vaga__dataEvento__gte=hoje
    )
    
    recusadas = candidaturas.filter(
        Q(status="recusada") |
        Q(status="pendente", vaga__dataEvento__lt=hoje)
    )
    
    aceitas = candidaturas.filter(status="aceito",
        vaga__dataEvento__gte=hoje)
    
    finalizadas = candidaturas.filter(
        Q(status="finalizado")|
        Q(status="aceito", vaga__dataEvento__lt=hoje)
    )
    
     # Verifica se cada candidatura já foi avaliada
    for candidatura in finalizadas:

        candidatura.avaliada = AvaliaVaga.objects.filter(
            freelancer=freelancer,
            vaga=candidatura.vaga
        ).exists()
        
    context = {
        "candidaturas": candidaturas,

        "pendentes": pendentes,
        "aceitas": aceitas,
        "recusadas": recusadas,
        "finalizadas": finalizadas,

        "total_analise": pendentes.filter(vaga__dataEvento__gte=hoje).count(),
        "total_aceitas": aceitas.filter( vaga__dataEvento__gte=hoje).count(),
        "total_recusadas": recusadas.count(),
        "total_finalizadas": finalizadas.count(),
    }

    return render(request, "candidaturas.html", context)

def cancelarCandidatura(request, candidatura_id):
    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    candidatura.delete()  
    messages.success(request, "Candidatura cancelada com sucesso!")
    return redirect("candidaturas")

