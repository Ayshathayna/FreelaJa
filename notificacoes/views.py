from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Notificacao

@login_required
def minhasNotificacoes(request):

    notificacoes_list = Notificacao.objects.filter(
        usuario=request.user
    ).order_by('-data_criacao')

    nao_lidas = notificacoes_list.filter(
        lida=False
    ).count()
    
    paginator = Paginator(notificacoes_list, 10)
    page_number = request.GET.get('page')
    
    try:
        notificacoes = paginator.page(page_number)
    except PageNotAnInteger:
        notificacoes = paginator.page(1)
    except EmptyPage:
        notificacoes = paginator.page(paginator.num_pages)
    
    base_template = (
        'baseEmpresa.html'
        if request.user.tipo_usuario == 'empresa'
        else 'baseFreelancer.html'
    )
    return render(
        request,
        'notificacoes.html',
        {
            'notificacoes': notificacoes,
            'nao_lidas': nao_lidas, 
            'base_template': base_template,
            'paginator': paginator,
        }
    )
@login_required
def abrirNotificacao(request, id):

    notificacao = get_object_or_404(
        Notificacao,
        id=id,
        usuario=request.user
    )

    notificacao.lida = True
    notificacao.save()

    if notificacao.link:
        return redirect(notificacao.link)

    return redirect('home')