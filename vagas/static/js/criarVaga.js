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


        btn.disabled = true;
        const campos = form.querySelectorAll(
            "input[required], textarea[required], select[required]"
        );
        function validar() {


            let completo = true;

            campos.forEach(
                campo => {

                    if (campo.type === 'file' || campo.type === 'hidden' || campo.type === 'checkbox' || campo.type === 'button') return;

                    if (
                        campo.value === null || campo.value === undefined || campo.value.toString().trim() === ""
                    ) {

                        completo = false;

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
        validar();

    });

document.addEventListener('DOMContentLoaded', () => {
    const detalhes = () => Array.from(document.querySelectorAll('input[name="detalhes"]'));
    const feedbackDetalhes = document.getElementById("detalhes-feedback");
    const hiddenCustom = document.querySelector('input[name="detalhes_custom"]');
    const customInput = document.getElementById('novo-detalhe-input');
    const addCustomBtn = document.getElementById('adicionar-detalhe');
    const customBadgesContainer = document.getElementById('custom-badges');

    let selectedCustom = {};

    function getCustomList() {
        if (!hiddenCustom) return [];
        const val = hiddenCustom.value || '';
        return val.split(',').map(s => s.trim()).filter(s => s.length > 0);
    }

    function setCustomList(list) {
        if (!hiddenCustom) return;
        hiddenCustom.value = list.join(', ');
    }

    function getSelectedCustomList() {
        // retorna apenas os custom que estão selecionados
        return Object.keys(selectedCustom).filter(k => selectedCustom[k]);
    }

    function renderCustomBadges() {
        if (!customBadgesContainer) return;
        customBadgesContainer.innerHTML = '';
        const list = getCustomList();
        list.forEach((text) => {
            const label = document.createElement('label');
            label.className = 'badge-option custom-badge';

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = selectedCustom[text] || false;

            const span = document.createElement('span');
            span.textContent = text;

            const btnRemove = document.createElement('button');
            btnRemove.type = 'button';
            btnRemove.className = 'remove-custom';
            btnRemove.textContent = '×';

            label.appendChild(checkbox);
            label.appendChild(span);
            label.appendChild(btnRemove);

            checkbox.addEventListener('change', () => {
                selectedCustom[text] = checkbox.checked;
                feedbackDetalhes.textContent = '';
            });

            customBadgesContainer.appendChild(label);
        });
    }

    function totalSelectedCount() {
        const checked = detalhes().filter(i => i.checked).length;
        const selectedCount = getSelectedCustomList().length;
        return checked + selectedCount;
    }

    const initialList = getCustomList();
    initialList.forEach(item => {
        selectedCustom[item] = true;
    });
    renderCustomBadges();

    // adicionar novo detalhe custom
    if (addCustomBtn) {
        addCustomBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const value = customInput.value.trim();
            if (!value) return;
            const list = getCustomList();
            const predefinedLabels = detalhes().map(i => i.nextSibling ? i.nextSibling.textContent.trim() : '').filter(Boolean);

            // impedir duplicatas entre custom e pré-definidos
            if (list.includes(value) || predefinedLabels.includes(value)) {
                feedbackDetalhes.textContent = 'Detalhe já existe.';
                return;
            }
            if (list.length >= 3) {
                feedbackDetalhes.textContent = 'Máximo de 3 detalhes personalizados.';
                return;
            }
            if (totalSelectedCount() >= 3) {
                feedbackDetalhes.textContent = 'Máximo de 3 detalhes no total.';
                return;
            }

            // adiciona como novo e marca como selecionado
            list.push(value);
            selectedCustom[value] = true;
            setCustomList(list);
            renderCustomBadges();
            customInput.value = '';
            feedbackDetalhes.textContent = '';
        });
    }

    // evento de clique no container de badges para remover
    if (customBadgesContainer) {
        customBadgesContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-custom')) {
                e.preventDefault();
                e.stopPropagation();
                const label = e.target.closest('.custom-badge');
                const span = label.querySelector('span');
                const text = span.textContent.trim();
                let list = getCustomList();
                list = list.filter(x => x !== text);
                delete selectedCustom[text];
                setCustomList(list);
                renderCustomBadges();
                feedbackDetalhes.textContent = '';
            }
        });
    }

    // controlar seleção de checkboxes considerando os custom selecionados
    detalhes().forEach((item) => {
        item.addEventListener('change', () => {
            const checkedCount = detalhes().filter(i => i.checked).length;
            const selectedCount = getSelectedCustomList().length;
            if (checkedCount + selectedCount > 3) {
                item.checked = false;
                feedbackDetalhes.textContent = 'Máximo de 3 detalhes no total.';
                return;
            }
            feedbackDetalhes.textContent = '';
        });
    });
});