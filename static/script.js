// Chamar as funções
setupMatriculaMask();
setupUserMenu();
setupDeleteModal();
setupFeedbackModal();


/**
 * Procura pelo campo MATRICULA e força a ser apenas números.
 */
function setupMatriculaMask() {
    // O Django gera o ID como 'id_nome-do-campo'
    const matriculaInput = document.getElementById("id_matricula");
    if (matriculaInput) {
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
    const menuTrigger = document.getElementById("user-menu-toggle");
    const userMenu = document.getElementById("user-menu-dropdown");
    const arrow = document.querySelector('.icon-arrow-toggle');
    if (menuTrigger && userMenu) {
        menuTrigger.addEventListener("click", function(event) {
            event.stopPropagation(); 
            userMenu.classList.toggle("show");
            if (arrow) arrow.classList.toggle('rotated');
        });
        window.addEventListener("click", function(event) {
            if (userMenu.classList.contains("show") && !userMenu.contains(event.target)) {
                userMenu.classList.remove("show");
                if (arrow) arrow.classList.remove('rotated');
            }
        });
    }
}

/**
 * Configura os gatilhos e ações do modal de exclusão na 'index.html'
 */
function setupDeleteModal() {
    // (Esta função ainda não está sendo usada, mas a deixamos pronta)
    const modal = document.getElementById('deleteModal');
    if (!modal) return; // Não estamos na página 'index'
    
    const backdrop = document.getElementById('deleteModalBackdrop');
    const deleteForm = document.getElementById('deleteModalForm');
    const collaboratorNameEl = document.getElementById('deleteModalColaboradorNome');
    const closeBtn = document.getElementById('closeModalBtn');
    const cancelBtn = document.getElementById('cancelModalBtn');
    const deleteTriggers = document.querySelectorAll('.delete-trigger');

    if (!deleteTriggers.length || !backdrop || !deleteForm) {
        return;
    }
    // ... (resto da lógica do modal de exclusão) ...
}


/**
 * Verifica se há mensagens de feedback (sucesso ou erro)
 * na página 'cadastro.html' e exibe o modal.
 */
function setupFeedbackModal() {
    const dataDiv = document.getElementById('feedbackData');
    const modal = document.getElementById('feedbackModal');
    
    // (IMPORTANTE) Se não for a página de cadastro, não faça nada.
    // Isso previne erros no console em outras páginas.
    if (!dataDiv || !modal) {
        return; 
    }

    const successMessage = dataDiv.dataset.successMessage;
    const errorMessage = dataDiv.dataset.errorMessage;

    const backdrop = document.getElementById('feedbackModalBackdrop');
    const header = document.getElementById('feedbackModalHeader');
    const title = document.getElementById('feedbackModalTitle');
    const body = document.getElementById('feedbackModalBody');
    const closeBtn = document.getElementById('feedbackModalCloseBtn');
    const okBtn = document.getElementById('feedbackModalOkBtn');

    const closeModal = () => {
        modal.style.display = 'none';
        backdrop.style.display = 'none';
        header.classList.remove('modal-header-success', 'modal-header-danger');
    };

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (okBtn) okBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    // Mostra o modal de SUCESSO
    if (successMessage) {
        title.textContent = 'Sucesso!';
        body.textContent = successMessage;
        header.classList.add('modal-header-success');
        modal.style.display = 'block';
        backdrop.style.display = 'block';
    } 
    // Mostra o modal de ERRO
    else if (errorMessage) {
        title.textContent = 'Falha no Cadastro';
        body.textContent = errorMessage;
        header.classList.add('modal-header-danger');
        modal.style.display = 'block';
        backdrop.style.display = 'block';
    }
}