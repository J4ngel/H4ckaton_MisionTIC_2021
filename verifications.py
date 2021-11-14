import re

#-----> VERIFICACIÓN POLITICAS DE SEGURIDAD PARA UNA CONTRASEÑA
def valid_pass(password):
    expresion_regular = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    if re.search(expresion_regular, password):
        return True
    else:
        return False

#-----> VALIDACIÓN DE DATOS PARA UN USUARIO EXTERNO (CLIENTE)
def valid_reg_1(cedula, name, gender, birthday, city, adds, username, phrase, password, check_pass, conditions):
    status = {'state':True, 'error': None}
    if conditions == 'None':
        status['state'] = False
        status['error'] = "Debe aceptar los terminos y condiciones"
        return status
    
    else:
        if len(cedula) == 0 or len(name) == 0 or gender == "0" or len(birthday) == 0 or len(city) == 0 or len(adds) == 0 or len(username) == 0 or len(phrase) == 0 or len(password) == 0 or len(check_pass) == 0:
            status['state'] = False
            status['error'] = "Algunos campos estan vacíos, verifiquelos y trate de nuevo"
            return status

        else:
            if not valid_pass(password):
                status['state'] = False
                status['error'] = "La contraseña debe contener minimo 8 caracteres, entre ellos: numeros, letras (mayus y min) y un caracter especial"
                return status

            else:
                if password != check_pass:
                    status['state'] = False
                    status['error'] = "Las contraseñas no coinciden"
                    return status
                
                else:
                    return status

#-----> VALIDACIÓN DE DATOS PARA UN USUARIO INTERNO (EMPLEADO)
def valid_reg_2(cedula, name, job, gender, birthday, city, adds, username, phrase, password, check_pass, conditions):
    status = {'state':True, 'error': None}
    if conditions == 'None':
        status['state'] = False
        status['error'] = "Debe aceptar los terminos y condiciones"
        return status
    
    else:
        if len(cedula) == 0 or len(name) == 0 or len(job) == 0 or gender == "0" or len(birthday) == 0 or len(city) == 0 or len(adds) == 0 or len(username) == 0 or len(phrase) == 0 or len(password) == 0 or len(check_pass) == 0:
            status['state'] = False
            status['error'] = "Algunos campos estan vacíos, verifiquelos y trate de nuevo"
            return status

        else:
            if not valid_pass(password):
                status['state'] = False
                status['error'] = "La contraseña debe contener minimo 8 caracteres, entre ellos: numeros, letras (mayus y min) y un caracter especial"
                return status

            else:
                if password != check_pass:
                    status['state'] = False
                    status['error'] = "Las contraseñas no coinciden"
                    return status
                
                else:
                    return status

#-----> VALIDACION CAJAS DE TEXTO LOGIN (CEDULA Y CONTRASEÑA)
def empity_login(username, password):
    status = {'state':True, 'error':None}

    if len(username) == 0:
        status['state'] = False
        status['error'] = "El campo de la cedula está vacío"
    elif len(password) == 0:
        status['state'] = False
        status['error'] = "El campo de la contraseña está vacío"
    return status

#-----> VALIDACION CAJAS DE TEXTO LOGIN DE RECUPERAR(NOMBRE, CUMPLEAÑOS Y FRASE)
def empity_recuperar_info(name, birthday, phrase):
    status = {'state':True, 'error':None}

    if len(name) == 0:
        status['state'] = False
        status['error'] = "El campo de nombre está vacío"
    elif len(phrase) == 0:
        status['state'] = False
        status['error'] = "El campo de la frase de seguridad está vacío"
    return status

def valid_recuperar_pass(password,check_pass):
    status = {'state':True, 'error': None}
    if len(password) == 0 or len(check_pass) == 0:
        status['state'] = False
        status['error'] = "Algunos campos estan vacíos, verifiquelos y trate de nuevo"
        return status
    else:
        if not valid_pass(password):
                status['state'] = False
                status['error'] = "La contraseña debe contener minimo 8 caracteres, entre ellos: numeros, letras (mayus y min) y un caracter especial"
                return status

        else:
            if password != check_pass:
                status['state'] = False
                status['error'] = "Las contraseñas no coinciden"
                return status
            else:
                return status