from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
'''
verificar 


-adicionar endereço na empresa é valido?(visto que os eventos podem ter endereços distintos
-um evento poderá ter mais de uma empresa? como coop
-o horário de inicio de evento, será oq o frela terá que estar no local? ou realmente o inicio do evento
-verifica se vai ficar só o endereço ou se vai ter campos separados para rua, número, bairro, cidade, estado e CEP
-verificar se é valido deixar a mensagem de risco 
'''