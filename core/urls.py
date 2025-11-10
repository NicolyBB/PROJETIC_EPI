# core/urls.py

from django.urls import path
from . import views  # Importa as views do app 'core'
from django.contrib.auth import views as auth_views # Importa as views de login/logout do Django

urlpatterns = [
    # 1. Página Inicial (/)
    # Chama a view 'home' que vamos criar no 'core/views.py'
    path('', views.home, name='home'),

    # 2. Página de Login (/login/)
    # Usa a view pronta do Django, mas diz para usar o NOSSO template 'login.html'
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # 3. Ação de Logout (/logout/)
    # Usa a view pronta do Django. Não precisa de template.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]