function togglePassword() {
    const input = document.getElementById("senha")  /*ainda não funciona*/

    if (input.type === "password") {
        input.type = "text"
        input.type.remove("password")
    } else {
        input.type = "password"
        input.type.remove("text")

    }
}


document.addEventListener("DOMContentLoaded", () => {

    /* ***********************************    TROCA ENTRE FREELANCER / EMPRESA     *********************************** */

    window.mostrarFormulario = function (tipo) {

        const freelancer = document.getElementById("freelancer")
        const empresa = document.getElementById("empresa")
        const buttons = document.querySelectorAll(".tab-btn")

        buttons.forEach(btn => btn.classList.remove("active"))

        if (tipo === "freelancer") {
            freelancer.classList.add("active")
            empresa.classList.remove("active")
            buttons[0].classList.add("active")
        } else {
            empresa.classList.add("active")
            freelancer.classList.remove("active")
            buttons[1].classList.add("active")
        }
    }


    function initStepper(formId) {

        const form = document.getElementById(formId)
        if (!form) return

        const steps = form.querySelectorAll(".step")
        const nextBtns = form.querySelectorAll(".next-btn")
        const backBtns = form.querySelectorAll(".back-btn")
        const dots = form.querySelectorAll(".dot")

        let current = 0

        function update() {

            steps.forEach((step, i) => {
                step.classList.remove("active")

                if (dots[i]) dots[i].classList.remove("active")

                if (i === current) {
                    step.classList.add("active")
                    if (dots[i]) dots[i].classList.add("active")
                }
            })
        }

        /* NEXT */
        nextBtns.forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.preventDefault()

                if (current < steps.length - 1) {
                    current++
                    update()
                }
            })
        })

        /* BACK */
        backBtns.forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.preventDefault()

                if (current > 0) {
                    current--
                    update()
                }
            })
        })

        update()
    }


    /* ***********************************    INIT DOS DOIS FORMULÁRIOS     *********************************** */

    initStepper("freelancerForm")
    initStepper("empresaForm")

})