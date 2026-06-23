"""sitefreela URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Inclui as URLs do aplicativo 'usuario'
    path('', include('usuario.urls')),  # Inclui as URLs do aplicativo 'core'
    path('perfis/', include('perfis.urls')),  # Inclui as URLs do aplicativo 'perfis'
    path('vagas/', include('vagas.urls')),  # Inclui as URLs do aplicativo 'vagas'
    path('avaliacoes/', include('avaliacoes.urls')),  # Inclui as URLs do aplicativo 'avaliacoes'
path(
    'notificacoes/',
    include('notificacoes.urls')
),

]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

from core import views

handler404 = 'core.views.erro404'
handler403 = 'core.views.erro403'
handler500 = 'core.views.erro500'