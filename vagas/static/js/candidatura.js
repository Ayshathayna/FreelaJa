
function mostrarFormulario(id, botao) { /* mostra o formulário correspondente(aceitas, pendentes, etc.) */

    document.querySelectorAll('.tab-content').forEach(tab => { // esconde todas as abas
        tab.style.display = 'none';
    });

    document.querySelectorAll('.filter-btn').forEach(btn => { // remove a classe active de todos os botões
        btn.classList.remove('active');
    });

    document.getElementById(id).style.display = 'grid'; // mostra a aba selecionada
    botao.classList.add('active');
}

document.addEventListener('DOMContentLoaded', function () {  // mostra a aba "Aceitas" por padrão ao carregar a página
    document.getElementById('aceitas').style.display = 'grid';

    document.querySelectorAll('.tab-content').forEach(tab => {
        if (tab.id !== 'aceitas') {
            tab.style.display = 'none';
        }
    });
});

function confirmarExclusao(event, url) {// exibe um alerta de confirmação antes de cancelar a candidatura
    event.preventDefault();

    Swal.fire({
        title: 'Cancelar candidatura?',
        text: 'Essa ação não pode ser desfeita.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sim, cancelar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#6b7280'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url;
        }
    });

    return false;
}