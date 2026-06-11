from . import views
from django.urls import path,include


urlpatterns = [

    path('', views.listarVagas, name='listarVagas'),
    path('criar/', views.criarVaga, name='criarVaga'),
    path('editar/<int:id>/',views.editarVaga, name='editarVaga'),
    path('excluir/<int:id>/', views.excluirVaga, name='excluirVaga'),
    path('ver/<int:id>/', views.verVaga, name='verVaga'),
    path('candidatar/<int:vaga_id>/', views.candidatarVaga, name='candidatarVaga'),
    path('candidaturas/', views.candidaturas, name='candidaturas'),
    path('cancelar/<int:candidatura_id>/', views.cancelarCandidatura, name='cancelarCandidatura'),
    path('vaga/<int:vaga_id>/candidatos/', views.candidatosVaga, name='candidatosVaga'),
    path('candidatura/<int:id>/aceitar/', views.aceitarCandidatura, name='aceitarCandidatura'),
    path('candidatura/<int:id>/recusar/', views.recusarCandidatura, name='recusarCandidatura'),

]