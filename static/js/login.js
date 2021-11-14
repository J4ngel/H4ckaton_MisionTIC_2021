let btn_datos = document.getElementById("btn_recuperar_datos")
let btn_pass = document.getElementById("btn_recuperar_pass")

btn_datos.addEventListener("click", r_datos)
btn_pass.addEventListener("click", r_pass)

function r_datos(){
    document.getElementById("form_login").action = "/login/recuperar_usuario"
}

function r_pass(){
    document.getElementById("form_login").action = "/login/recuperar_contraseña"
}