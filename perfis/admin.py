from django.contrib import admin

# Register your models here.
from .models import Empresa, Freelancer

admin.site.register(Empresa)
admin.site.register(Freelancer)