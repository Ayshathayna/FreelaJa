function confirmarVolta(event, url) {
    event.preventDefault();
    console.log("Confirmação de volta acionada");
    Swal.fire({
        title: 'Voltar para a página de vagas?',
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

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const input =
            document.querySelector(
                'input[type="file"]'
            );

        const preview =
            document.getElementById(
                "preview-image"
            );

        input.addEventListener(
            "change",
            function () {

                const file =
                    this.files[0];

                if (file) {

                    const reader =
                        new FileReader();

                    reader.onload =
                        function (e) {

                            preview.src =
                                e.target.result;

                        }

                    reader.readAsDataURL(
                        file
                    );
                }

            }
        );

    }
);
document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.querySelector(
                "form"
            );

        const btn =
            document.querySelector(
                ".btn-save"
            );

        const campos =
            form.querySelectorAll(
                "input, textarea, select"
            );

        btn.disabled = true;

        function validar() {

            let completo = true;

            campos.forEach(
                campo => {

                    if (
                        campo.type !== "file"
                    ) {

                        if (
                            campo.value.trim() === ""
                        ) {

                            completo = false;

                        }

                    }

                }

            );

            btn.disabled =
                !completo;

        }

        campos.forEach(
            campo => {

                campo.addEventListener(
                    "input",
                    validar
                );

                campo.addEventListener(
                    "change",
                    validar
                );

            }

        );

    });