# Importações necessárias do Django
# ================================
from django.shortcuts import render, redirect, get_object_or_404 
from .models import Colaborador
from django.db.models import Q
from django.contrib import messages # <--- Importado da sua versão anterior

# View (Função) para a página de LISTA de Colaboradores (index.html)
# =================================================================
def colaborador_lista(request):
    query = request.GET.get('q', '')
    
    if query:
        colaboradores = Colaborador.objects.filter(
            Q(nome_completo__icontains=query) |
            Q(cpf__icontains=query) |
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
        'search_query': query 
    }
    return render(request, 'index.html', context)


# View (Função) para a página de CADASTRO de Colaboradores (cadastro.html)
# ======================================================================
def colaborador_novo(request):
    if request.method == 'POST':
        cpf_limpo = ''.join(filter(str.isdigit, request.POST.get('cpf')))
        
        # --- VERIFICAÇÃO DE CPF DUPLICADO ---
        # Antes de criar, verifica se algum colaborador no banco já possui este CPF.
        if Colaborador.objects.filter(cpf=cpf_limpo).exists():
            # Se sim, envia uma mensagem de erro para o template.
            messages.error(request, 'ERRO: O CPF digitado já está cadastrado.')
            # Prepara o contexto para devolver os dados que o usuário digitou.
            context = {
                'form_data': request.POST 
            }
            # Renderiza a página de cadastro novamente (sem redirecionar),
            # mostrando o erro e mantendo os dados no formulário.
            return render(request, 'cadastro.html', context)
        # --- FIM DA VERIFICAÇÃO ---

        # Se o CPF NÃO existe, prossegue com a criação.
        Colaborador.objects.create(
            nome_completo=request.POST.get('nome_completo'),
            cpf=cpf_limpo, 
            funcao=request.POST.get('funcao'),
            status=request.POST.get('status')
        )
        
        # Envia uma mensagem de sucesso.
        messages.success(request, 'Colaborador cadastrado com sucesso!')
        return redirect('index')

    # Se for um GET (apenas carregando a página)
    return render(request, 'cadastro.html')


# View (Função) para a página de EDIÇÃO de Colaboradores (reutiliza cadastro.html)
# ==============================================================================
def colaborador_editar(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if request.method == 'POST':
        cpf_limpo = ''.join(filter(str.isdigit, request.POST.get('cpf')))

        # --- VERIFICAÇÃO DE CPF DUPLICADO (PARA EDIÇÃO) ---
        # Verifica se existe OUTRO colaborador (excluindo o atual) com o mesmo CPF.
        # .exclude(id=id) é crucial aqui.
        if Colaborador.objects.filter(cpf=cpf_limpo).exclude(id=id).exists():
            messages.error(request, 'ERRO: O CPF digitado já pertence a outro colaborador.')
            context = {
                'colaborador': colaborador, # Dados originais para o título, etc.
                'form_data': request.POST  # Dados que o usuário tentou salvar
            }
            # Renderiza a página de edição novamente com o erro.
            return render(request, 'cadastro.html', context)
        # --- FIM DA VERIFICAÇÃO ---

        # Se passou na verificação, atualiza o objeto.
        colaborador.nome_completo = request.POST.get('nome_completo')
        colaborador.cpf = cpf_limpo
        colaborador.funcao = request.POST.get('funcao')
        colaborador.status = request.POST.get('status')
        colaborador.save()
        
        messages.success(request, 'Colaborador atualizado com sucesso!')
        return redirect('index')

    # Se for um GET (carregando a página de edição pela primeira vez)
    context = {'colaborador': colaborador}
    return render(request, 'cadastro.html', context)


# View (Função) para EXCLUIR um Colaborador
# =========================================
def colaborador_excluir(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    colaborador.delete()
    # Adiciona uma mensagem de sucesso após excluir
    messages.success(request, f'Colaborador "{colaborador.nome_completo}" foi excluído.')
    return redirect('index')