"""
Risco de atraso / conflito de agenda entre eventos de um freelancer.

Regras:
- sobreposição de horário (começo antes do término do outro) => CONFLITO (bloqueia).
- deslocamento insuficiente ou apertado => apenas AVISO de risco para as duas
  partes; não bloqueia. Se ambas concordarem, a candidatura segue.

Cálculo tempo de deslocamento: distância em linha
reta (Haversine) entre as coordenadas dos eventos, dividida por uma velocidade média
urbana e multiplicada por um fator de desvio.

"""

from datetime import datetime, timedelta
from math import radians, sin, cos, asin, sqrt


# ---- parâmetros do cálculo ----
VELOCIDADE_MEDIA_KMH = 30      # velocidade média urbana assumida
FATOR_DESVIO = 1.3             # ruas não são linha reta
MARGEM_RISCO_MIN = 30          # folga (min) acima do trajeto ainda considerada "apertada"
JANELA_ANALISE_MIN = 360       # só analisamos eventos a até 6h de distância um do outro
BUFFER_SEM_COORD_MIN = 60      # fallback sem coordenadas: intervalo mínimo entre locais diferentes


def _intervalo(vaga):
    #Retorna (inicio, fim) como datetime, tratando eventos que viram a madrugada.
    inicio = datetime.combine(vaga.dataEvento, vaga.horarioInicio)
    fim = datetime.combine(vaga.dataEvento, vaga.horarioFim)
    if fim <= inicio:
        fim += timedelta(days=1)
    return inicio, fim


def _haversine_km(lat1, lon1, lat2, lon2):
    #Distância em linha reta (km) entre dois pontos.
    raio = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * raio * asin(sqrt(a))


def _tem_coordenadas(vaga):
    return vaga.latitude is not None and vaga.longitude is not None


def _tempo_viagem_min(a, b):
    #Tempo estimado de deslocamento (min) entre dois eventos, ou None se faltar coordenada.
    if not (_tem_coordenadas(a) and _tem_coordenadas(b)):
        return None
    km = _haversine_km(a.latitude, a.longitude, b.latitude, b.longitude)
    return (km / VELOCIDADE_MEDIA_KMH) * 60 * FATOR_DESVIO


def _neutro():
    return {'conflito': False, 'risco': False, 'motivo': '', 'risco_msg': ''}


def comparar_vagas(vaga, outra):
    #Compara um par de vagas. Retorna o dict de resultado (conflito/risco) ou None se não há impedimento/risco entre elas.
    inicio_n, fim_n = _intervalo(vaga)
    ini_o, fim_o = _intervalo(outra)

    if inicio_n < fim_o and ini_o < fim_n:
        return {
            'conflito': True,
            'risco': False,
            'motivo': f'Conflito de horário com a vaga "{outra.titulo}" ({outra.dataEvento}).',
            'risco_msg': '',
        }

    # intervalo livre entre os dois eventos
    if fim_o <= inicio_n:
        gap = (inicio_n - fim_o).total_seconds() / 60
    elif fim_n <= ini_o:
        gap = (ini_o - fim_n).total_seconds() / 60
    else:
        return None

    if gap > JANELA_ANALISE_MIN:
        return None

    tempo = _tempo_viagem_min(outra, vaga)

    if tempo is not None:
        if gap < tempo:
            return {
                'conflito': False,
                'risco': True,
                'motivo': '',
                'risco_msg': (
                    f'Tempo de deslocamento provavelmente insuficiente em relação à vaga "{outra.titulo}": '
                    f'trajeto estimado ~{int(round(tempo))} min e intervalo de apenas {int(round(gap))} min. '
                    f'Risco alto de atraso.'
                ),
            }
        if gap < tempo + MARGEM_RISCO_MIN:
            return {
                'conflito': False,
                'risco': True,
                'motivo': '',
                'risco_msg': (
                    f'Deslocamento apertado em relação à vaga "{outra.titulo}": '
                    f'trajeto estimado ~{int(round(tempo))} min e intervalo de {int(round(gap))} min. '
                    f'Pode haver risco de atraso.'
                ),
            }
    else:
        # Sem coordenadas: usa um buffer fixo entre locais diferentes
        end_o = (outra.endereco or '').strip().lower()
        end_n = (vaga.endereco or '').strip().lower()
        if gap < BUFFER_SEM_COORD_MIN and end_o != end_n:
            return {
                'conflito': False,
                'risco': True,
                'motivo': '',
                'risco_msg': (
                    f'Intervalo curto ({int(round(gap))} min) em relação à vaga "{outra.titulo}", '
                    f'em endereço diferente. Pode haver risco de atraso.'
                ),
            }

    return None


def avaliar_para_lista(freelancer, vagas):
    #Anota cada vaga da lista com .conflito_msg e .risco_msg (para os botões da listagem).
    from .models import Candidatura

    aceitas = [
        c.vaga for c in
        Candidatura.objects
        .filter(freelancer=freelancer, status='aceito')
        .select_related('vaga')
    ]

    for vaga in vagas:
        conflito_msg = ''
        risco_msg = ''
        for outra in aceitas:
            if outra.id == vaga.id:
                continue
            r = comparar_vagas(vaga, outra)
            if not r:
                continue
            if r['conflito']:
                conflito_msg = r['motivo']
                break
            if r['risco'] and not risco_msg:
                risco_msg = r['risco_msg']
        vaga.conflito_msg = conflito_msg
        vaga.risco_msg = risco_msg

    return vagas


def analisar_risco_atraso(freelancer, vaga):
    #Compara a 'vaga' com os eventos já aceitos do freelancer.
    
    from .models import Candidatura

    aceitas = (
        Candidatura.objects
        .filter(freelancer=freelancer, status='aceito')
        .select_related('vaga')
        .exclude(vaga_id=vaga.id)
    )

    resultados = []
    for c in aceitas:
        r = comparar_vagas(vaga, c.vaga)
        if r:
            resultados.append(r)

    # conflito tem prioridade sobre risco
    for r in resultados:
        if r['conflito']:
            return r
    for r in resultados:
        if r['risco']:
            return r

    return _neutro()
