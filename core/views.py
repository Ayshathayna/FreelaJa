from django.shortcuts import render
from perfis.models import Empresa
from vagas.models import Vaga
# Create your views here.
def homeFreelancer(request):
    vagas = Vaga.objects.all()
    return render(request, 'homeFreelancer.html', {
        'vagas': vagas
        })

def homeEmpresa(request):

    #empresa = request.user.empresa  # empresa logada

    vagas = Vaga.objects.all()

    return render(request, 'homeEmpresa.html', {
        'vagas': vagas
    })
