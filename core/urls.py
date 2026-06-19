from django.urls import path
from . import views

urlpatterns = [
    path('', views.site, name='site'),
    path('home/', views.homeFreelancer, name='homeFreelancer'),
    path('home-empresa/', views.homeEmpresa, name='homeEmpresa'),

]