from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from django.shortcuts import render, redirect

from .models import Usuario
from perfis.models import Freelancer, Empresa
from notificacoes.utils import verificar_perfil_freelancer


from .forms import (
    CadastroFreelancerForm,
    CadastroEmpresaForm,
    LoginForm
)


def sair(request):

    logout(request)

    messages.success(
        request,
        "Logout realizado com sucesso!"
    )

    return redirect('login')

def login(request):

    form = LoginForm()

    if request.method == "POST":
        
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.get_user()

            auth_login(request, usuario)
            if hasattr(request.user, "freelancer"):

                verificar_perfil_freelancer(
                    request.user.freelancer
                )

            if usuario.tipo_usuario == "empresa":
                return redirect("homeEmpresa")

            return redirect("homeFreelancer")

        messages.error(
            request,
            "Email ou senha inválidos."
        )

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )


def cadastro(request):

    freelancer_form = CadastroFreelancerForm()
    empresa_form = CadastroEmpresaForm()

    if request.method == "POST":
        tipo = request.POST.get("tipo")

        # ==========================================
        # FREELANCER
        # ==========================================

        if tipo == "freelancer":

            freelancer_form = CadastroFreelancerForm(
                request.POST
            )

            if freelancer_form.is_valid():

                freelancer_form.save()

                messages.success(
                    request,
                    "Cadastro realizado com sucesso!"
                )

                return redirect("login")

        # ==========================================
        # EMPRESA
        # ==========================================

        elif tipo == "empresa":

            empresa_form = CadastroEmpresaForm(
                request.POST
            )

            if empresa_form.is_valid():

                empresa_form.save()

                messages.success(
                    request,
                    "Empresa cadastrada com sucesso!"
                )

                return redirect("login")

    return render(
        request,
        "cadastro.html",
        {
            "freelancer_form": freelancer_form,
            "empresa_form": empresa_form,
        }
    )