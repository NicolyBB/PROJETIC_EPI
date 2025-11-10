# Importações necessárias do Django
# ================================
from django.shortcuts import render, redirect, get_object_or_404 
from .models import Colaborador
from .forms import ColaboradorForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# =================================================================
# View (Função) para a página de LISTA (index.html)
# (ESTA FUNÇÃO ESTAVA FALTANDO NO SEU CÓDIGO)
# =================================================================
@login_required
def colaborador_lista(request):
    query = request.GET.get('q', '')
    
    if query:
        colaboradores = Colaborador.objects.filter(
            Q(nome_completo__icontains=query) |
            Q(matricula__icontains=query) |
            Q(funcao__icontains=query)
        ).order_by('-data_cadastro')
    else:
        colaboradores = Colaborador.objects.all().order_by('-data_cadastro')
    
    total_colaboradores = colaboradores.count()
    colaboradores_ativos = colaboradores.filter(status='Ativo').count()
    colaboradores_inativos = total_colaboradores - colaboradores_ativos

    context = {
        'colaboradores_lista': colaboradores,
        'total_colaboradores': total_colaboradores,
        'colaboradores_ativos': colaboradores_ativos,
        'colaboradores_inativos': colaboradores_inativos,
        'search_query': query,
        'messages': messages.get_messages(request) # Para os modais de exclusão/edição
    }
    return render(request, 'index.html', context)


# ======================================================================
# View (Função) para a página de CADASTRO (cadastro.html)
# (Esta é a sua nova view, que usa o script.js)
# ======================================================================
@login_required 
def colaborador_novo(request):
    # Define o contexto inicial. Sempre teremos um form.
    context = {'form': ColaboradorForm()}

    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            
            # --- SUCESSO ---
            # Envia a mensagem de sucesso que o seu JS 'setupFeedbackModal' espera
            context['success_message'] = "Colaborador cadastrado com sucesso!"
            # (Envia um form limpo para a página)
            context['form'] = ColaboradorForm() 
            
        else:
            # --- ERRO ---
            # Se o form for inválido (ex: matrícula duplicada), envia a mensagem de erro
            if form.errors:
                # Pega o primeiro erro (ex: 'Esta matrícula já está cadastrada.')
                first_error = next(iter(form.errors.values()))[0]
                context['error_message'] = f"ERRO: {first_error}"
            else:
                context['error_message'] = "Erro desconhecido. Verifique os campos."
            
            # Envia o formulário PREENCHIDO (inválido) de volta para o usuário
            context['form'] = form

    # Renderiza o template UMA ÚNICA VEZ, com o contexto (seja de sucesso, erro, ou novo)
    return render(request, 'cadastro.html', context)


# ==============================================================================
# View (Função) para a página de EDIÇÃO (reutiliza cadastro.html)
# ==============================================================================
@login_required
def colaborador_editar(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador alterado com sucesso!')
            return redirect('index') # Redireciona para a lista
    else:
        form = ColaboradorForm(instance=colaborador) # Pré-preenche

    context = {
        'form': form,
        'colaborador': colaborador
    }
    return render(request, 'cadastro.html', context)


# =========================================
# View (Função) para EXCLUIR um Colaborador
# =========================================
@login_required
def colaborador_excluir(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == 'POST':
        nome_colaborador = colaborador.nome_completo
        colaborador.delete()
        messages.success(request, f'Colaborador "{nome_colaborador}" foi excluído.')
    
    return redirect('index')