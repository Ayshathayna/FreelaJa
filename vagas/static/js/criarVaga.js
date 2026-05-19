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