from .models import Notificacao

# CRIAÇÃO GENÉRICA DE NOTIFICAÇÃO
# Função reutilizável para todo o sistema
def criar_notificacao(
    usuario,
    titulo,
    mensagem,
    tipo='sistema',  
    link=None
):

    Notificacao.objects.create(
        usuario=usuario,
        titulo=titulo,
        mensagem=mensagem,
        tipo=tipo,    
        link=link

    )



def verificar_perfil_freelancer(freelancer):

    problemas = []

    if not freelancer.foto:
        problemas.append("foto")

    if not freelancer.experiencia:
        problemas.append("experiência")

    if len(freelancer.interesses) < 3:
        problemas.append("interesses")

    if problemas:

        criar_notificacao(
            usuario=freelancer.usuario,
            titulo="Perfil incompleto",
            mensagem="Complete seu perfil para aumentar suas chances de contratação.",
            tipo="perfil",
            link="/perfis/meuPerfil/"
        )