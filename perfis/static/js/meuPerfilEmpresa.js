function togglePassword(id, element){

    const input = document.getElementById(id);
    const icon = element.querySelector("i");

    if(input.type === "password"){

        input.type = "text";

        icon.classList.replace(
            "fa-eye",
            "fa-eye-slash"
        );

    }else{

        input.type = "password";

        icon.classList.replace(
            "fa-eye-slash",
            "fa-eye"
        );

    }
}

const fotoInput =
    document.getElementById("id_foto");

if(fotoInput){

    fotoInput.addEventListener(
        "change",
        function(){

            document.getElementById(
                "file-name"
            ).textContent =
            this.files.length
            ? this.files[0].name
            : "Nenhum arquivo selecionado";

        }
    );

}