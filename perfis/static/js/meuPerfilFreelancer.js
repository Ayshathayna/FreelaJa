function togglePassword(id, element){

    const input = document.getElementById(id);
    const icon = element.querySelector("i");

    if(input.type === "password"){

        input.type = "text";

        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");

    }else{

        input.type = "password";

        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");

    }
}

document.addEventListener("DOMContentLoaded", () => {

    // FOTO

    const fotoInput = document.getElementById("id_foto");

    if(fotoInput){

        fotoInput.addEventListener("change", function(){

            const nome = this.files.length
                ? this.files[0].name
                : "Nenhum arquivo selecionado";

            document.getElementById("file-name")
                .textContent = nome;

        });

    }

    // INTERESSES

    const interesses = document.querySelectorAll(
        'input[name="interesses"]'
    );

    const feedbackInteresses =
        document.getElementById(
            "interesses-feedback"
        );

    function showError(feedback, mensagem){

        feedback.textContent = mensagem;
        feedback.style.color = "#ef4444";

    }

    function hideError(feedback){

        feedback.textContent = "";

    }

    interesses.forEach((item) => {

        item.addEventListener("change", () => {

            const selecionados =
                document.querySelectorAll(
                    'input[name="interesses"]:checked'
                );

            if(selecionados.length > 5){

                item.checked = false;

                showError(
                    feedbackInteresses,
                    "Máximo de 5 interesses."
                );

                return;
            }

            if(selecionados.length < 3){

                showError(
                    feedbackInteresses,
                    "Escolha pelo menos 3 interesses."
                );

                return;
            }

            hideError(
                feedbackInteresses
            );

        });

    });

    // SUBMIT

    const form = document.querySelector("form");

    if(form){

        form.addEventListener("submit", function(e){

            const selecionados =
                document.querySelectorAll(
                    'input[name="interesses"]:checked'
                );

            if(
                selecionados.length < 3 ||
                selecionados.length > 5
            ){

                e.preventDefault();

                showError(
                    feedbackInteresses,
                    "Não é possivel salvar. Selecione entre 3 e 5 interesses."
                );

            }

        });

    }

});