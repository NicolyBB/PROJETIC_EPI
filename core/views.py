# core/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Esta é a view da sua página INICIAL (home.html)
def home(request):
    # 'render' apenas exibe o template
    return render(request, 'home.html')