let btn_frase = document.getElementById("btn_frase")
let btn_pass = document.getElementById("btn_pass")

btn_frase.addEventListener("click", actualizar_frase)
btn_pass.addEventListener("click", actualizar_pass)

function actualizar_frase(){
    document.getElementById("form_usuario_externo").action = "/usuario/act_frase"
}

function actualizar_pass(){
    document.getElementById("form_usuario_externo").action = "/usuario/act_pass"
}