from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.homeFreelancer, name='homeFreelancer'),
    path('homeEmpresa/', views.homeEmpresa, name='homeEmpresa'),
    path('', views.site, name='site'),
    
]