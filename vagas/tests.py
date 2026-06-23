from datetime import date, time
from django.test import SimpleTestCase
from vagas.models import Vaga
from vagas.risco_atraso import comparar_vagas

# Dois pontos dentro de Chapecó (~5,3 km / ~14 min de trajeto estimado)
FEIRA_EFAPI = (-27.1006, -52.6720)   # Parque de Exposições / feira (bairro Efapi)
PRACA_CENTRO = (-27.0966, -52.6186)  # Praça Coronel Bertaso (centro)

def _vaga(titulo, hi, hf, lat=None, lon=None, endereco="Local", d=date(2026, 7, 10)):
    return Vaga(
        titulo=titulo,
        dataEvento=d,
        horarioInicio=hi,
        horarioFim=hf,
        latitude=lat,
        longitude=lon,
        endereco=endereco,
    )


class ComparaVagasTests(SimpleTestCase):
    """
    Testes de unidade da regra de risco de atraso, entre dois locais de Chapecó:
    a feira no Efapi e a Praça Coronel Bertaso (centro).
    """

    def test_sobreposicao_de_horario_gera_conflito(self):
        # Feira no Efapi e evento na praça com horários sobrepostos -> conflito (bloqueia)
        feira = _vaga("Feira no Efapi", time(18, 0), time(23, 0), *FEIRA_EFAPI)
        praca = _vaga("Evento na Praça do Centro", time(20, 0), time(22, 0), *PRACA_CENTRO)

        resultado = comparar_vagas(feira, praca)

        self.assertIsNotNone(resultado)
        self.assertTrue(resultado["conflito"])
        self.assertFalse(resultado["risco"])

    def test_efapi_para_praca_sem_tempo_gera_risco(self):
        # Feira no Efapi (10h-12h) -> Praça (12h05) = 5 min p/ ~14 min de trajeto -> risco
        feira = _vaga("Feira no Efapi", time(10, 0), time(12, 0), *FEIRA_EFAPI)
        praca = _vaga("Evento na Praça do Centro", time(12, 5), time(13, 0), *PRACA_CENTRO)

        resultado = comparar_vagas(feira, praca)

        self.assertIsNotNone(resultado)
        self.assertTrue(resultado["risco"])
        self.assertFalse(resultado["conflito"])

    def test_efapi_para_praca_apertado_gera_risco(self):
        # Feira no Efapi (10h-12h) -> Praça (12h20) = 20 min (pouco acima dos ~14) -> apertado
        feira = _vaga("Feira no Efapi", time(10, 0), time(12, 0), *FEIRA_EFAPI)
        praca = _vaga("Evento na Praça do Centro", time(12, 20), time(13, 0), *PRACA_CENTRO)

        resultado = comparar_vagas(feira, praca)

        self.assertIsNotNone(resultado)
        self.assertTrue(resultado["risco"])
        self.assertFalse(resultado["conflito"])

    def test_efapi_para_praca_com_folga_nao_gera_nada(self):
        # Feira no Efapi (10h-12h) -> Praça (13h) = 60 min, tempo de sobra -> sem risco/conflito
        feira = _vaga("Feira no Efapi", time(10, 0), time(12, 0), *FEIRA_EFAPI)
        praca = _vaga("Evento na Praça do Centro", time(13, 0), time(14, 0), *PRACA_CENTRO)

        self.assertIsNone(comparar_vagas(feira, praca))
