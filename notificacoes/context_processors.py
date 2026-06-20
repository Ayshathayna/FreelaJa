from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Notificacao


@login_required
def minhasNotificacoes(request):

    notificacoes = (
        Notificacao.objects
        .filter(usuario=request.user)
        .order_by('-data_criacao')
    )

    nao_lidas = notificacoes.filter(
        lida=False
    ).count()

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
            'base_template': base_template
        }
    )

def notificacoes_nao_lidas(request):

    if request.user.is_authenticated:

        total = Notificacao.objects.filter(
            usuario=request.user,
            lida=False
        ).count()

    else:
        total = 0

    return {
        'notificacoes_nao_lidas': total
    }

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

    if request.user.tipo_usuario == "empresa":
        return redirect("homeEmpresa")

    return redirect("home")