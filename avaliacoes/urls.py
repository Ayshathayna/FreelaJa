from . import views
from django.urls import path,include

urlpatterns = [
    
    path('avaliarVaga/<int:candidatura_id>/', views.avaliarVaga, name='avaliarVaga'),
    path('verAvaliacao/<int:candidatura_id>/', views.verAvaliacao, name='verAvaliacao'),
]