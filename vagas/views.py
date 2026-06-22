from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from avaliacoes.models import AvaliaVaga, AvaliaFreelancer
from perfis.models import Empresa, Freelancer
from .models import Vaga, Candidatura
from .forms import VagaForm
from notificacoes.utils import criar_notificacao


#--------------------------------------------------------- EMPRESA --------------------------------------------------------------------
@login_required
def criarVaga(request):
    empresa = get_object_or_404(Empresa, usuario=request.user)

    if request.method == 'POST': #verifica se o método da requisição é POST, ou seja, se o formulário foi submetido. Se for, ele processa os dados do formulário.

        form = VagaForm(request.POST,request.FILES)

        if form.is_valid():  #verifica se os dados do formulário são válidos. Se forem, ele salva a vaga no banco de dados.

            vaga = form.save(commit=False) #form.save(commit=False) salva os dados do formulário, mas não os envia para o banco de dados ainda. Isso permite que você faça modificações adicionais na instância do modelo antes de salvá-la.                   
            vaga.empresa = empresa
            vaga.save()  #salva a vaga no banco de dados.
            
            messages.success(request, "Vaga criada com sucesso!")
            return redirect('homeEmpresa')
    else:
        form = VagaForm() 

    return render(request, 'criarEditarVaga.html',
        {
            'form': form
        }
    )

@login_required
def editarVaga(request,id):
    empresa = get_object_or_404(Empresa, usuario=request.user)
    vaga = get_object_or_404(Vaga,id=id)
    
    if vaga.empresa != empresa:
        raise PermissionDenied()
    
    form = VagaForm(request.POST or None, request.FILES or None, instance=vaga)

    if request.method == "POST" and form.is_valid():

        form.save()
        candidaturas = Candidatura.objects.filter(
            vaga=vaga
        )

        for candidatura in candidaturas:

            criar_notificacao(
                usuario=candidatura.freelancer.usuario,
                titulo='Vaga atualizada',
                mensagem=f'A vaga "{vaga.titulo}" recebeu alterações.',
                tipo='atualizada',
                link=reverse(
                    'verVaga',
                    args=[vaga.id]
                )
            )
        messages.success(request, "Vaga editada com sucesso!")
        return redirect("homeEmpresa")

    return render(
        request,
        "criarEditarVaga.html",
        {
            "form": form,
            "editar": True,
            "vaga": vaga
        }
    )
    
@login_required
def cancelarVaga(request, id):
    empresa = get_object_or_404(Empresa, usuario=request.user)

    vaga = get_object_or_404(Vaga, id=id)
    if vaga.empresa != empresa:
        raise PermissionDenied()

    candidaturas = Candidatura.objects.filter(
        vaga=vaga
    )

    for candidatura in candidaturas:

        criar_notificacao(
            usuario=candidatura.freelancer.usuario,
            titulo='Vaga cancelada',
            mensagem=f'A vaga "{vaga.titulo}" foi cancelada pela empresa.',
            tipo='cancelada',
            link=reverse('verVaga',
            args=[candidatura.vaga.id])
        )

    vaga.status = 'cancelado'
    vaga.save()

    candidaturas.update(
        status='recusado'
    )

        
    messages.success(request, "Vaga cancelada com sucesso!")
    return redirect(
        "homeEmpresa"
    )



#------------------------------------------------------------------
@login_required
def candidatosVaga(request, vaga_id):
    empresa = get_object_or_404(Empresa, usuario=request.user)
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if vaga.empresa != empresa:
        raise PermissionDenied()
    
    hoje = timezone.now().date()

    candidaturas = Candidatura.objects.filter(
        vaga=vaga
    ).select_related('freelancer', 'freelancer__usuario')
    
    vagaFinalizada = ( 
        vaga.status == "finalizado"
        or vaga.dataEvento < hoje
    )
    
    pendentes = candidaturas.filter( 
        status="pendente",
        vaga__dataEvento__gte=hoje
    )
    
    recusadas = candidaturas.filter(
        Q(status="recusado") |
        Q(status="pendente", vaga__dataEvento__lt=hoje)
    )
    
    aceitas = candidaturas.filter(status="aceito")
    
    avaliadas_ids = set(
        AvaliaFreelancer.objects.filter(
            empresa=empresa
        ).values_list('freelancer_id',  flat=True)
    )
    for candidatura in aceitas:
        candidatura.avaliada = candidatura.freelancer_id in avaliadas_ids
    context = {
        "vaga": vaga,
        "candidaturas": candidaturas,
        "vagaFinalizada": vagaFinalizada,

        "pendentes": pendentes,
        "aceitas": aceitas,
        "recusadas": recusadas,

        "total_analise": pendentes.count(),
        "total_aceitas": aceitas.count(),
        "total_recusadas": recusadas.count(),
    }

    return render(request, 'candidatos.html', context)

@login_required
def aceitarCandidatura(request, id):
    candidatura = get_object_or_404(Candidatura, id=id)
    empresa = get_object_or_404(Empresa, usuario=request.user)
    if candidatura.vaga.empresa != empresa:
        raise PermissionDenied()
    
    if(candidatura.vaga.quantidadeVagas <= candidatura.vaga.quantidadeSelecionados):
        messages.error(request, "Não há vagas disponíveis para aceitar mais candidatos.")
        return redirect('candidatosVaga', vaga_id=candidatura.vaga.id)
    
    with transaction.atomic():

        if candidatura.status != "aceito" and candidatura.vaga.quantidadeSelecionados < candidatura.vaga.quantidadeVagas:

            candidatura.status = "aceito"
            candidatura.save()

            candidatura.vaga.quantidadeSelecionados += 1
            candidatura.vaga.save()
            
    criar_notificacao(
        usuario=candidatura.freelancer.usuario,
        titulo='Você foi aprovado!',
        mensagem=f'Parabéns! Você foi aprovado para a vaga {candidatura.vaga.titulo}',
        tipo='aceito', 
        link=reverse(
            'verVaga',
            args=[candidatura.vaga.id]
        )
    )
    
    messages.success(request, "Candidato aceito com sucesso!")
    return redirect('candidatosVaga', vaga_id=candidatura.vaga.id)

@login_required
def recusarCandidatura(request, id):
    candidatura = get_object_or_404(Candidatura, id=id)
    empresa = get_object_or_404(Empresa, usuario=request.user)

    if candidatura.vaga.empresa != empresa:
        raise PermissionDenied()
    
    with transaction.atomic():

        if candidatura.status == "aceito":
            candidatura.vaga.quantidadeSelecionados -= 1
            candidatura.vaga.save()

        candidatura.status = "recusado"
        candidatura.save()
    criar_notificacao(
        usuario=candidatura.freelancer.usuario,
        titulo='Candidatura encerrada',
        mensagem=f'Você não foi selecionado para a vaga {candidatura.vaga.titulo}',
        tipo='recusado',
        link=reverse(
            'verVaga',
            args=[candidatura.vaga.id]
        )
    )
    messages.warning(request, "Candidato recusado.")
    return redirect('candidatosVaga', vaga_id=candidatura.vaga.id)


@login_required
def finalizarVaga(request, vaga_id):
    empresa = get_object_or_404(Empresa, usuario=request.user)
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if vaga.empresa != empresa:
        raise PermissionDenied()
    
    vaga.status = "finalizado"
    vaga.save()
    
    Candidatura.objects.filter(
        vaga=vaga,
        status="pendente"
    ).update(status="recusado")
    candidaturas_aceitas = Candidatura.objects.filter(
    vaga=vaga,
    status='aceito'
)
    for candidatura in candidaturas_aceitas:

        criar_notificacao(
            usuario=candidatura.freelancer.usuario,
            titulo='Vaga finalizada',
            mensagem=f'A vaga {vaga.titulo} foi finalizada. Avalie a empresa.',
            tipo='avaliacao',
            link=reverse(
                'avaliarVaga',
                args=[vaga.id]
            )
        )
     # Notificação para a empresa
    criar_notificacao(
        usuario=empresa.usuario,
        titulo='Avaliações disponíveis',
        mensagem=f'A vaga "{vaga.titulo}" foi finalizada. Avalie os freelancers participantes.',
        tipo='avaliacao',
        link=reverse(
            'candidatosVaga',
            args=[vaga.id]
        )
    )
    messages.success(request, "Vaga finalizada com sucesso!")
    return redirect('homeEmpresa')


#--------------------------------------------------------- FREELANCER --------------------------------------------------------------------
@login_required
def verVaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    vaga.atualizar_status()

    eh_empresa = Empresa.objects.filter(
            usuario=request.user,
            id=vaga.empresa.id
        ).exists()
    ja_candidatou = False

    if not eh_empresa:
        freelancer = Freelancer.objects.filter(
            usuario=request.user
        ).first()

        if freelancer:
            ja_candidatou = Candidatura.objects.filter(
                freelancer=freelancer,
                vaga=vaga
            ).exists()
    context = {
        "jaCandidatou": ja_candidatou,
        'vaga': vaga,
        'eh_empresa': eh_empresa,
        'base_template':
            'baseEmpresa.html' if eh_empresa else 'baseFreelancer.html'
    }

    return render(request, 'verVaga.html', context)
    
@login_required
def candidatarVaga(request, vaga_id):
    url_anterior = request.META.get('HTTP_REFERER')

    vaga = get_object_or_404(Vaga, id=vaga_id)
    freelancer = get_object_or_404(Freelancer, usuario=request.user)
    if vaga.status != "aberto":
        messages.error(request, "Esta vaga não está mais aberta.")
        return redirect("verVaga", id=vaga.id)
    if Candidatura.objects.filter(vaga=vaga, freelancer=freelancer).exists():
        messages.warning(request, "Você já se candidatou para esta vaga.")
        return redirect("verVaga", id=vaga.id)

    Candidatura.objects.get_or_create(vaga=vaga, freelancer=freelancer)
    criar_notificacao(
        usuario=vaga.empresa.usuario,
        titulo='Nova candidatura',
        mensagem=f'{freelancer.nomeCompleto} se candidatou à vaga "{vaga.titulo}".',
        tipo='candidatura',
        link=reverse(
            'candidatosVaga',
            args=[vaga.id]
        )
    )

    messages.success(request, "Candidatura enviada com sucesso!")

    if url_anterior:
        return redirect(url_anterior)

    return redirect('verVaga', id=vaga.id)


@login_required
def cancelarCandidatura(request, candidatura_id):
    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    
    if candidatura.status == 'aceito':

        candidatura.vaga.quantidadeSelecionados -= 1

        if candidatura.vaga.quantidadeSelecionados < 0:
            candidatura.vaga.quantidadeSelecionados = 0
        criar_notificacao(
            usuario=candidatura.vaga.empresa.usuario,
            titulo='Freelancer desistiu da vaga',
            mensagem=f'{candidatura.freelancer.nomeCompleto} desistiu da vaga "{candidatura.vaga.titulo}".',
            tipo='warning',
            link=reverse(
                'candidatosVaga',       
                args=[candidatura.vaga.id]
            )
        )

        candidatura.vaga.save()
    candidatura.delete()  
    messages.success(request, "Candidatura cancelada com sucesso!")
    return redirect("candidaturas")


#-----------------------------------------------------------------------------------------
@login_required
def listarVagas(request):

    query = request.GET.get('q', '').strip() or request.GET.get('busca', '').strip()
    categoria = request.GET.get('categoria', '').strip()

    freelancer = get_object_or_404(
        Freelancer,
        usuario=request.user
    )

    for vaga in Vaga.objects.filter(status='aberto'):
        vaga.atualizar_status()

    vagas = Vaga.objects.filter(status='aberto')

    if query:
        query_lower = query.lower()
        matching_categories = [
            key for key, label in Vaga.CATEGORIAS
            if query_lower in key.lower() or query_lower in label.lower()
        ]

        search_filter = (
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query) |
            Q(endereco__icontains=query) |
            Q(empresa__nomeFantasia__icontains=query) |
            Q(detalhes__icontains=query)
        )

        if matching_categories:
            search_filter |= Q(categoria__in=matching_categories)

        vagas = vagas.filter(search_filter)

    if categoria:
        vagas = vagas.filter(categoria=categoria)

    candidaturas_ids = set(
        Candidatura.objects.filter(
            freelancer=freelancer
        ).values_list('vaga_id', flat=True)
    )

    for vaga in vagas:
        vaga.jaCandidatou = vaga.id in candidaturas_ids

    return render(request, 'vagas.html', {
        'vagas': vagas,
        'query': query,
        'categoria_selecionada': categoria,
        'categorias': Vaga.CATEGORIAS,
    })


@login_required
def candidaturas(request):
    freelancer = get_object_or_404(Freelancer, usuario=request.user)
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
        Q(status="recusado") |
        Q(status="pendente", vaga__dataEvento__lt=hoje)
    )
    

    aceitas = candidaturas.filter(
        status="aceito",
        vaga__dataEvento__gte=hoje,
    ).exclude(vaga__status="finalizado")
    
    finalizadas = candidaturas.filter(
        Q(vaga__status="finalizado")&
        Q(status="aceito", vaga__dataEvento__lt=hoje)
    )
    avaliadas_ids = set(
        AvaliaVaga.objects.filter(
            freelancer=freelancer
        ).values_list('vaga_id', flat=True)
    )
     # Verifica se cada candidatura já foi avaliada
    for candidatura in finalizadas:
        candidatura.avaliada = candidatura.vaga_id in avaliadas_ids

        
    context = {
        "candidaturas": candidaturas,

        "pendentes": pendentes,
        "aceitas": aceitas,
        "recusadas": recusadas,
        "finalizadas": finalizadas,

        "total_analise": pendentes.count(),
        "total_aceitas": aceitas.count(),
        "total_recusadas": recusadas.count(),
        "total_finalizadas": finalizadas.count(),
    }

    return render(request, "candidaturas.html", context)
