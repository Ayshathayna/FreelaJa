from django.contrib import admin

# Register your models here.
from .models import Vaga, Candidatura

admin.site.register(Vaga)
admin.site.register(Candidatura)