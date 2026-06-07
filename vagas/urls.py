from . import views
from django.urls import path,include


urlpatterns = [

    path('criar/', views.criarVaga, name='criarVaga'),
    path('editar/<int:id>/',views.editarVaga, name='editarVaga'),
    path('excluir/<int:id>/', views.excluirVaga, name='excluirVaga'),
    path('ver/<int:id>/', views.verVaga, name='verVaga'),
    path('candidatar/<int:vaga_id>/', views.candidatarVaga, name='candidatarVaga'),
    path('candidaturas/', views.candidaturas, name='candidaturas'),
    path('cancelar/<int:candidatura_id>/', views.cancelarCandidatura, name='cancelarCandidatura'),

]