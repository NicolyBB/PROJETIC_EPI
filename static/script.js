// Função principal que é executada quando o DOM está pronto
document.addEventListener("DOMContentLoaded", function() {
    
    // Tenta configurar a máscara de CPF (só roda na página de cadastro)
    setupCpfMask();

    // Tenta configurar o menu do usuário (roda em todas as páginas)
    setupUserMenu();
    
    // Tenta configurar o modal de exclusão (só roda na 'index.html')
    setupDeleteModal();

    // (NOVO) Tenta configurar o modal de feedback (só roda na 'cadastro.html')
    setupFeedbackModal();
});

/**
 * Procura pelo formulário e campo MATRICULA (removendo máscara de CPF)
 */
function setupCpfMask() {
    // A função de máscara de CPF não é mais necessária para matrícula
    // Vamos apenas checar se o input existe
    const matriculaInput = document.getElementById("matricula");
    if (matriculaInput) {
        // Você pode adicionar validação de 'apenas números' aqui se desejar
        matriculaInput.addEventListener('input', function(e) {
            // Remove qualquer coisa que não seja dígito
            e.target.value = e.target.value.replace(/\D/g, '');
        });
    }
}

/**
 * Configura o menu dropdown do usuário na sidebar
 */
function setupUserMenu() {
    const menuTrigger = document.getElementById("user-menu-trigger");
    const userMenu = document.getElementById("user-menu");

    if (menuTrigger && userMenu) {
        menuTrigger.addEventListener("click", function(event) {
            event.stopPropagation(); 
            userMenu.classList.toggle("show");
        });

        window.addEventListener("click", function(event) {
            if (userMenu.classList.contains("show") && !userMenu.contains(event.target)) {
                userMenu.classList.remove("show");
            }
        });
    }
}


/**
 * Configura os gatilhos e ações do modal de exclusão na 'index.html'
 */
function setupDeleteModal() {
    const modal = document.getElementById('deleteModal');
    const backdrop = document.getElementById('deleteModalBackdrop');
    const deleteForm = document.getElementById('deleteModalForm');
    const collaboratorNameEl = document.getElementById('deleteModalColaboradorNome');
    const closeBtn = document.getElementById('closeModalBtn');
    const cancelBtn = document.getElementById('cancelModalBtn');
    const deleteTriggers = document.querySelectorAll('.delete-trigger');

    if (!modal || !deleteTriggers.length || !backdrop || !deleteForm) {
        return; // Não é a página index.html, então pare
    }

    const openModal = (url, nome) => {
        deleteForm.action = url; 
        collaboratorNameEl.textContent = nome; 
        modal.style.display = 'block';
        backdrop.style.display = 'block';
    };

    const closeModal = () => {
        modal.style.display = 'none';
        backdrop.style.display = 'none';
    };

    deleteTriggers.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault(); 
            const url = this.href;
            const nome = this.getAttribute('data-nome');
            openModal(url, nome);
        });
    });

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);
}


/**
 * (NOVA FUNÇÃO)
 * Verifica se há mensagens de feedback (sucesso ou erro)
 * na página 'cadastro.html' e exibe o modal.
 */
function setupFeedbackModal() {
    // Pega os elementos do DOM
    const dataDiv = document.getElementById('feedbackData');
    const modal = document.getElementById('feedbackModal');
    const backdrop = document.getElementById('feedbackModalBackdrop');
    const header = document.getElementById('feedbackModalHeader');
    const title = document.getElementById('feedbackModalTitle');
    const body = document.getElementById('feedbackModalBody');
    const closeBtn = document.getElementById('feedbackModalCloseBtn');
    const okBtn = document.getElementById('feedbackModalOkBtn');

    // Se não estiver na página 'cadastro.html', dataDiv será null.
    if (!dataDiv || !modal || !backdrop) {
        return;
    }

    // Pega as mensagens dos atributos data-*
    const successMessage = dataDiv.dataset.successMessage;
    const errorMessage = dataDiv.dataset.errorMessage;

    const closeModal = () => {
        modal.style.display = 'none';
        backdrop.style.display = 'none';
        // Limpa as classes de cor para a próxima vez
        header.classList.remove('modal-header-success', 'modal-header-danger');
    };

    // Adiciona os eventos para fechar o modal
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (okBtn) okBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    // Verifica se há mensagem de SUCESSO
    if (successMessage) {
        title.textContent = 'Sucesso!';
        body.textContent = successMessage;
        header.classList.add('modal-header-success');
        modal.style.display = 'block';
        backdrop.style.display = 'block';
    } 
    // Senão, verifica se há mensagem de ERRO
    else if (errorMessage) {
        title.textContent = 'Falha no Cadastro';
        body.textContent = errorMessage; // Ex: "ERRO: Esta matrícula já está cadastrada."
        header.classList.add('modal-header-danger');
        modal.style.display = 'block';
        backdrop.style.display = 'block';
    }
}