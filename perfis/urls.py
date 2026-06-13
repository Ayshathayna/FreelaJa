from . import views
from django.urls import path,include

urlpatterns = [
    path('freelancer/<int:freelancer_id>/<int:candidatura_id>/', views.perfilFreelancer, name='perfilFreelancer'),
    path('empresa/<int:empresa_id>/', views.perfilEmpresa, name='perfilEmpresa'),
]