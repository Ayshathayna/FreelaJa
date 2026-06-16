from django.shortcuts import render, get_object_or_404, redirect
from vagas.models import Candidatura, Vaga
from .models import Freelancer, Empresa
from avaliacoes.models import AvaliaFreelancer, AvaliaVaga
from django.contrib import messages
from .forms import PerfilFreelancerForm,PerfilEmpresaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


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
    
    
@login_required
def meuPerfilFreelancer(request):

    freelancer = get_object_or_404(Freelancer, usuario=request.user)

    if request.method == "POST":

        form = PerfilFreelancerForm(
            request.POST,
            request.FILES,
            instance=freelancer
        )

        if form.is_valid():

            senha = form.cleaned_data.get( 'nova_senha' )
            confirmar = form.cleaned_data.get('confirmar_senha'  )

            if senha and senha != confirmar:

                messages.error(
                    request,
                    "As senhas não coincidem."
                )

            else:

                form.save()
                update_session_auth_hash(
                        request,
                        request.user
                    )
                messages.success(
                    request,
                    "Perfil atualizado!"
                )
                return redirect('homeFreelancer')

    else:

        form = PerfilFreelancerForm(
            instance=freelancer
        )

    return render(
        request,
        "meuPerfilFreelancer.html",
        {
            "form": form,
            "freelancer": freelancer
        }
    )
    

@login_required
def meuPerfilEmpresa(request):

    empresa = get_object_or_404(Empresa, usuario=request.user)

    if request.method == "POST":

        form = PerfilEmpresaForm(
            request.POST,
            request.FILES,
            instance=empresa
        )

        if form.is_valid():

            senha = form.cleaned_data.get("nova_senha")
            confirmar = form.cleaned_data.get("confirmar_senha")

            if senha and senha != confirmar:

                messages.error(
                    request,
                    "As senhas não coincidem."
                )

            else:

                form.save()
                update_session_auth_hash(
                        request,
                        request.user
                    )
                messages.success(
                    request,
                    "Perfil atualizado com sucesso!"
                )
                return redirect('homeEmpresa')


    else:

        form = PerfilEmpresaForm(
            instance=empresa
        )

    return render(
        request,
        "meuPerfilEmpresa.html",
        {
            "empresa": empresa,
            "form": form
        }
    )