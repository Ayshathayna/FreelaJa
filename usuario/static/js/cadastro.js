function togglePassword(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);

    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}



document.addEventListener("DOMContentLoaded", () => {

    /* ===================== UTIL ===================== */

    function showError(input, feedback, message) {
        feedback.textContent = message;
        feedback.style.display = "block";
        feedback.style.color = "red";
        input.style.borderColor = "red";
    }

    function hideError(input, feedback) {
        feedback.textContent = "";
        feedback.style.display = "none";
        input.style.borderColor = "";
    }

    /* ===================== FORM TROCA ===================== */

    window.mostrarFormulario = function (tipo) {

        const freelancer = document.getElementById("freelancer");
        const empresa = document.getElementById("empresa");
        const buttons = document.querySelectorAll(".tab-btn");

        if (!freelancer || !empresa) return;

        buttons.forEach(btn => btn.classList.remove("active"));

        if (tipo === "freelancer") {
            freelancer.classList.add("active");
            empresa.classList.remove("active");
            buttons[0]?.classList.add("active");
        } else {
            empresa.classList.add("active");
            freelancer.classList.remove("active");
            buttons[1]?.classList.add("active");
        }
        setTimeout(() => {
            verificarSenhasIguais();
        }, 0);
    };

    /* ===================== STEPPER ===================== */

    function initStepper(formId) {
        const form = document.getElementById(formId);
        if (!form) return;

        const steps = form.querySelectorAll(".step");
        const nextBtns = form.querySelectorAll(".next-btn");
        const backBtns = form.querySelectorAll(".back-btn");
        const dots = form.querySelectorAll(".dot");
        const submitBtn = form.querySelector('button[type="submit"]');

        let current = 0;

        function update() {
            steps.forEach((step, i) => {
                const active = i === current;

                step.classList.toggle("active", active);
                if (dots[i]) dots[i].classList.toggle("active", active);
            });
            updateStepActions();
        }

        function isStepValid(step) {
            let valido = true;

            const inputs = step.querySelectorAll("input, select, textarea");
            inputs.forEach(input => {
                if (!input.checkValidity()) {
                    valido = false;
                }
            });

            const email = step.querySelector('input[type="email"]');
            if (email && email.value && !validarEmail(email.value)) {
                valido = false;
            }

            const cpf = step.querySelector("#id_cpf");
            if (cpf && cpf.value.replace(/\D/g, "").length !== 11) {
                valido = false;
            }

            const cnpj = step.querySelector("#id_cnpj");
            if (cnpj && cnpj.value.replace(/\D/g, "").length !== 14) {
                valido = false;
            }

            const senha = step.querySelector('input[id^="id_password_"]');
            const confirmar = step.querySelector('input[id^="id_confirmar_senha_"]');
            if (senha && confirmar) {
                if (senha.value.trim() !== confirmar.value.trim()) {
                    valido = false;
                }
            }

            if (step.id === "step-interesses") {
                const interesses = step.querySelectorAll('input[name="interesses"]:checked');
                if (interesses.length < 3) {
                    valido = false;
                }
            }

            if (step.id === "step-sobre-empresa") {
                const descricao = step.querySelector('textarea[name="descricao"]');
                if (descricao && !descricao.value.trim()) {
                    valido = false;
                }
            }

            return valido;
        }

        function updateStepActions() {
            // Os botões permanecem sempre clicáveis. A validação acontece no
            // clique (validarStep), que exibe os erros e bloqueia o avanço.
            // Não desabilitamos os botões aqui para evitar que o usuário fique
            // preso (ex.: após um erro do servidor os campos de senha voltam
            // vazios e travariam o botão "Próximo").
            isStepValid(steps[current]);
        }

        function attachStepInputListeners() {
            form.addEventListener("input", () => {
                updateStepActions();
            });

            form.addEventListener("change", () => {
                updateStepActions();
            });
        }

        function validarStep(step) {
            let valido = true;

            const inputs = step.querySelectorAll("input, select, textarea");

            inputs.forEach(input => {
                if (!input.checkValidity()) {
                    input.reportValidity();
                    valido = false;
                }
            });

            const email = step.querySelector('input[type="email"]');
            if (email && email.value && !validarEmail(email.value)) {
                showError(email, document.getElementById("email-feedback-" + getAbaAtiva()), "Email inválido");
                valido = false;
            }

            const cpf = step.querySelector("#id_cpf");
            if (cpf && cpf.value.replace(/\D/g, "").length !== 11) {
                valido = false;
            }

            const cnpj = step.querySelector("#id_cnpj");
            if (cnpj && cnpj.value.replace(/\D/g, "").length !== 14) {
                valido = false;
            }

            const aba = getAbaAtiva();
            const senha = document.getElementById("id_password_" + aba);
            const confirmar = document.getElementById("id_confirmar_senha_" + aba);

            if (senha && confirmar) {
                if (senha.value.trim() !== confirmar.value.trim()) {
                    showError(confirmar, document.getElementById("confirmar-feedback_" + aba), "Senhas não coincidem");
                    valido = false;
                }
            }

            if (step.id === "step-interesses") {
                const interesses = step.querySelectorAll('input[name="interesses"]:checked');
                const feedback = step.querySelector("#interesses-feedback");
                if (interesses.length < 3) {
                    showError(step.querySelector('input[name="interesses"]'), feedback, "Escolha pelo menos 3 interesses");
                    valido = false;
                }
            }

            if (step.id === "step-sobre-empresa") {
                const descricao = step.querySelector('textarea[name="descricao"]');
                if (descricao && !descricao.value.trim()) {
                    const feedback = step.querySelector("#descricao-feedback");
                    showError(descricao, feedback, "Descreva sua empresa");
                    valido = false;
                }
            }

            return valido;
        }
        nextBtns.forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.preventDefault();

                const step = steps[current];

                const valido = validarStep(step);

                if (!valido) {
                    step.classList.add("step-error");
                    return; // bloqueia avanço
                }

                // remove erro se estiver válido
                step.classList.remove("step-error");

                if (current < steps.length - 1) {
                    current++;
                    update();
                }
            });
        });

        backBtns.forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.preventDefault();

                if (current > 0) {
                    current--;
                    update();
                }
            });
        });

        attachStepInputListeners();

        form.addEventListener("submit", (e) => {
            const step = steps[current];
            const valido = validarStep(step);
            if (!valido) {
                step.classList.add("step-error");
                e.preventDefault();
            }
        });

        update();
    }

    initStepper("freelancerForm");
    initStepper("empresaForm");

    /* ===================== CPF / CNPJ ===================== */

    function formatCpf(value) {
        const digits = value.replace(/\D/g, "").slice(0, 11);
        return digits
            .replace(/(\d{3})(\d)/, "$1.$2")
            .replace(/(\d{3})(\d)/, "$1.$2")
            .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    }

    function formatCnpj(value) {
        const digits = value.replace(/\D/g, "").slice(0, 14);
        return digits
            .replace(/(\d{2})(\d)/, "$1.$2")
            .replace(/(\d{3})(\d)/, "$1.$2")
            .replace(/(\d{3})(\d)/, "$1/$2")
            .replace(/(\d{4})(\d{1,2})$/, "$1-$2");
    }

    function applyDocumentoMask(input, formatter) {
        if (!input) return;

        input.addEventListener("input", () => {
            const cursorPos = input.selectionStart;
            const oldValue = input.value;
            const formatted = formatter(oldValue);
            input.value = formatted;

            if (cursorPos !== null) {
                input.setSelectionRange(formatted.length, formatted.length);
            }
        });
    }

    function formatCelular(value) {
        const d = value.replace(/\D/g, "").slice(0, 11);
        if (d.length <= 10) {
            return d
                .replace(/(\d{2})(\d)/, "($1) $2")
                .replace(/(\d{4})(\d{1,4})$/, "$1-$2");
        }
        return d
            .replace(/(\d{2})(\d)/, "($1) $2")
            .replace(/(\d{5})(\d{1,4})$/, "$1-$2");
    }

    applyDocumentoMask(document.getElementById("id_cpf"), formatCpf);
    applyDocumentoMask(document.getElementById("id_cnpj"), formatCnpj);
    applyDocumentoMask(document.getElementById("id_celular"), formatCelular);

    /* ===================== SENHAS ===================== */

    function getAbaAtiva() {
        return document.getElementById("empresa")?.classList.contains("active")
            ? "empresa"
            : "freelancer";
    }

    function getSenhaInputs() {
        const aba = getAbaAtiva();

        return {
            senha: document.getElementById("id_password_" + aba),
            confirmar: document.getElementById("id_confirmar_senha_" + aba)
        };
    }

    function verificarSenhasIguais() {
        const aba = getAbaAtiva();

        const senha = document.getElementById("id_password_" + aba);
        const confirmar = document.getElementById("id_confirmar_senha_" + aba);
        const feedback = document.getElementById("confirmar-feedback_" + aba);


        if (!senha || !confirmar || !feedback) return;

        const senhaVal = senha.value.trim();
        const confVal = confirmar.value.trim();

        if (!senhaVal || !confVal) {
            hideError(confirmar, feedback);
            return;
        }

        if (senhaVal !== confVal) {
            showError(confirmar, feedback, "Senhas não coincidem");
        } else {
            hideError(confirmar, feedback);
        }

    }

    /* 🔥 ESCUTA QUALQUER DIGITAÇÃO NOS CAMPOS DE SENHA */
    document.addEventListener("input", (e) => {
        if (
            e.target.id.includes("id_password_") ||
            e.target.id.includes("id_confirmar_senha_")
        ) {
            verificarSenhasIguais();
        }
    });


    /* ===================== CPF / CNPJ ===================== */

    function validarDocumento(input, feedback, length, label) {
        if (!input || !feedback) return;

        input.addEventListener("input", () => {
            const value = input.value.replace(/\D/g, "");

            if (value.length === 0 || value.length === length) {
                hideError(input, feedback);
                return;
            }

            showError(input, feedback, `${label} inválido`);
        });
    }

    validarDocumento(
        document.getElementById("id_cpf"),
        document.getElementById("cpf-feedback"),
        11,
        "CPF"
    );

    validarDocumento(
        document.getElementById("id_cnpj"),
        document.getElementById("cnpj-feedback"),
        14,
        "CNPJ"
    );

    /* ===================== INTERESSES ===================== */

    const interesses = document.querySelectorAll('input[name="interesses"]');
    const feedbackInteresses = document.getElementById("interesses-feedback");

    interesses.forEach((item) => {
        item.addEventListener("change", () => {

            const selecionados = document.querySelectorAll('input[name="interesses"]:checked');

            if (selecionados.length > 5) {
                item.checked = false;
                showError(item, feedbackInteresses, "Máximo de 5 interesses");
                return;
            }

            if (selecionados.length < 3) {
                showError(item, feedbackInteresses, "Escolha pelo menos 3 interesses");
                return;
            }

            hideError(item, feedbackInteresses);
        });
    });

    /* ===================== EMAIL ===================== */

    function validarEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function initEmail(input, feedback) {
        if (!input || !feedback) return;

        input.addEventListener("input", () => {

            const value = input.value;

            if (!value) {
                hideError(input, feedback);
                return;
            }

            if (!validarEmail(value)) {
                showError(input, feedback, "Email inválido");
            } else {
                hideError(input, feedback);
            }
        });
    }

    initEmail(
        document.getElementById("id_email"),
        document.getElementById("email-feedback-freelancer")
    );

    initEmail(
        document.querySelector("#empresaForm #id_email"),
        document.getElementById("email-feedback-empresa")
    );

});
