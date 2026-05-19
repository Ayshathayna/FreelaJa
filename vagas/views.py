from django.shortcuts import render, redirect,     get_object_or_404
from perfis.models import  Empresa
from .models import Vaga
from .forms import VagaForm
from datetime import date



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

            return redirect(
                'homeEmpresa'
            )
        else:
            print(form.errors) #se o formulário não for válido, ele imprime os erros no console para ajudar na depuração. Isso pode ser útil para identificar quais campos do formulário estão causando problemas de validação.
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

    vaga = get_object_or_404(
        Vaga,
        id=id
    )

    if request.method == "POST":

        form = VagaForm(
            request.POST,
            request.FILES,
            instance=vaga
        )

        if form.is_valid():

            form.save()

            return redirect(
                "homeEmpresa"
            )

    else:

        form = VagaForm(
            instance=vaga
        )

    return render(
        request,
        "criarEditarVaga.html",
        {
            "form": form,
            "editar": True,
            "vaga": vaga
        }
    )