from django.urls import path
from .views import minhasNotificacoes, abrirNotificacao
from . import views

urlpatterns = [
    path(
        '',
        minhasNotificacoes,
        name='notificacoes'
    ),
    path(
    'notificacao/<int:id>/', views.abrirNotificacao,
    name='abrirNotificacao'
)
]