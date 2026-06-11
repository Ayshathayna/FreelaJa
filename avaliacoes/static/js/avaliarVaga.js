function confirmarVolta(event, url) {
    event.preventDefault();
    console.log("Confirmação de volta acionada");
    Swal.fire({
        title: 'Voltar para a página de candidaturas?',
        text: 'Você perderá as informações não salvas.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sim, voltar',
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