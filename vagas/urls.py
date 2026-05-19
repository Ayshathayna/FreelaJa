from . import views
from django.urls import path,include


urlpatterns = [

    path('criar/', views.criarVaga, name='criarVaga'),
    path('editar/<int:id>/',views.editarVaga, name='editarVaga'
),

]