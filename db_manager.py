import sqlite3
from sqlite3 import Error

import hashlib
from werkzeug.security import check_password_hash

from flask import g
import main

#------>CONEXIÓN A LA BASE DE DATOS
def sql_connection():
    try:
        if 'con' not in g:
            path = main.confBd()
            g.con = sqlite3.connect(path + "orion.db")
        return g.con
    except Error:
        print(Error)

#----->REGISTRO DE UN USUARIO EXTERNO (CLIENTE)
def reg_1(cedula, name, gender, birthday, city, adds, username,phrase, password, rol):
    status={'state':True, 'error':None}
    
    try:
        con=sql_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO Usuarios(Cedula, Nombre_y_apellido, Sexo, Fecha_de_nacimiento, Direccion, Ciudad, Contrasena, rol, frase, username) VALUES (?,?,?,?,?,?,?,?,?,?)",(cedula,name,gender,birthday,adds,city,password, rol,phrase,username))
        con.commit()
        if con.total_changes > 0:
            return status
        else:
            status['state']=False
            status['error']="No se pudo registrar el usuario"
            return status
            
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status

#----->REGISTRO DE UN USUARIO INTERNO (EMPLEADO)
def reg_2(cedula, name, job, gender, birthday, city, adds,username, phrase, password, rol):
    status={'state':True, 'error':None}
    try:
        con=sql_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO Usuarios(Cedula, Nombre_y_apellido, Sexo, Fecha_de_nacimiento, Direccion, Ciudad, Contrasena, rol, frase,Cargo,username) VALUES (?,?,?,?,?,?,?,?,?,?,?)",(cedula,name,gender,birthday,adds,city,password,rol,phrase,job,username))
        con.commit()
        if con.total_changes > 0:
            return status
        else:
            status['state']=False
            status['error']="No se pudo registrar el empleado"
            return status
            
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status

#----->VERIFICACION DE CREDENCIALES      
def login_session(username, password):
    status = {'state':True, 'error':None, 'data':None}
    try:
        con=sql_connection()
        cur = con.cursor()
        query=cur.execute("SELECT Contrasena, Nombre_y_apellido, rol,id_usuario FROM Usuarios WHERE username=?",[username]).fetchone()
        if query!=None:
            if check_password_hash(query[0],password):
                status['data']= [query[1], query[2], query[3]]
                return status
            else:
                status['state'] = False
                status['error'] = "Credenciales incorrectas, verifique la entrada e intente de nuevo"
                return status
                
        else:
            status['state'] = False
            status['error'] = "El usuario digitado no existe"
            return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status

#----->DEVUELVE EL username SI LAS TRES PREGUNTAS SE RESUELVEN DE FORMA CORRECTA
def recuperar_usuario(name, birthday, phrase):
    status = {'state':True, 'error':None, 'data':None}
    try:
        con=sql_connection()
        cur = con.cursor()
        query=cur.execute("SELECT username, frase, id_usuario FROM Usuarios WHERE Nombre_y_apellido=? AND Fecha_de_nacimiento=?",[name,birthday]).fetchone()
        if query!=None:
            if check_password_hash(query[1],phrase):
                status['data']= [query[0],query[2]]
                return status
            else:
                status['state'] = False
                status['error'] = "Verificación de datos erronea, intente nuevamente"
                return status
                
        else:
            status['state'] = False
            status['error'] = "Verificación de datos erronea, intente nuevamente"
            return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status

#----->ACTUALIZA LA CONTRASEÑA SI SE CUMPLIERON LAS VERIFICACIONES ANTERIORES
def recuperar_pass(password,id_usuario):
    status = {'state':True, 'error':None, 'data':None}
    try:
        con=sql_connection()
        cur = con.cursor()
        cur.execute("UPDATE Usuarios SET Contrasena=? WHERE id_usuario=?",[password,id_usuario])
        con.commit()
        if con.total_changes > 0:
            status['data']="Contraseña actualizada con exito"
            return status
        else:
            status['state']=False
            status['error']="No se pudo actualizar la contraseña"
            return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status

#----->ACTUALIZA LA IFNORMACION GENERAL CON id_usuario
def actualizar_info(id_usuario, name, addr, city):
    status = {'state':True, 'error':None, 'data':None}
    try:
        con=sql_connection()
        cur = con.cursor()
        cur.execute("UPDATE Usuarios SET Nombre_y_apellido=?, Direccion=?, Ciudad=? WHERE id_usuario=?",[name,addr,city,id_usuario])
        con.commit()
        if con.total_changes > 0:
            status['data']="Datos actualizados con exito"
            return status
        else:
            status['state']=False
            status['error']="No se pudo actualizar"
            return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status

#-------->ACTUALIZAR FRASE CON id_usuario
def actualizar_frase(id_usuario, phrase, password):
    status = {'state':True, 'error':None, 'data':None}
    try:
        con=sql_connection()
        cur = con.cursor()

        query=cur.execute("SELECT Contrasena FROM Usuarios WHERE id_usuario=?",[id_usuario]).fetchone()
        if query!=None:
            if check_password_hash(query[0],password):
                        cur.execute("UPDATE Usuarios SET frase=? WHERE id_usuario=?",[phrase,id_usuario])
                        con.commit()
                        if con.total_changes > 0:
                            status['data']="Frase de seguridad actualizada con exito"
                            return status
                        else:
                            status['state']=False
                            status['error']="No se pudo actualizar la frase"
                            return status
            else:
                status['state'] = False
                status['error'] = "Contraseña actual erronea, intente nuevamente"
                return status
                
        else:
            status['state'] = False
            status['error'] = "Fallo la busqueda"
            return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status

#------>ACTUALIZAR LA CONTRASEÑA CON id_usuario
def actualizar_pass(id_usuario, new_pass, password):
    status = {'state':True, 'error':None, 'data':None}
    try:
        con=sql_connection()
        cur = con.cursor()

        query=cur.execute("SELECT Contrasena FROM Usuarios WHERE id_usuario=?",[id_usuario]).fetchone()
        if query!=None:
            if check_password_hash(query[0],password):
                        cur.execute("UPDATE Usuarios SET Contrasena=? WHERE id_usuario=?",[new_pass,id_usuario])
                        con.commit()
                        if con.total_changes > 0:
                            status['data']="Contraseña actualizada con exito"
                            return status
                        else:
                            status['state']=False
                            status['error']="No se pudo actualizar la contraseña"
                            return status
            else:
                status['state'] = False
                status['error'] = "Contraseña actual erronea, intente nuevamente"
                return status
                
        else:
            status['state'] = False
            status['error'] = "Fallo la busqueda"
            return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status
#------>ELIMINAR CUENTAS POR id_usuario
def eliminar_cuenta(id_usuario):
    status = {'state':True, 'error':None, 'data':None}
    try:
        con=sql_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM Usuarios WHERE id_usuario = ?",[id_usuario])
        con.commit()
        if con.total_changes > 0:
            status['data']="Cuenta eliminada con exito"
            return status
        else:
            status['state']=False
            status['error']="No se pudo eliminar la cuenta"
            return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status

#------>DEVUELVE EL id_usuario SI ENCUENTRA COINCIDENCIA
def editar_usuarios(cedula, rol):
    status = {'state':True, 'error':None, 'data':None}
    try:
        con=sql_connection()
        cur = con.cursor()
        query=cur.execute("SELECT id_usuario FROM Usuarios WHERE Cedula=? AND rol=?",[cedula,rol]).fetchone()
        if query!=None:
            status['data']= query[0]
            return status           
        else:
            status['state'] = False
            status['error'] = "La cedula no se encuentra registrada, verifique los datos e intente nuevamente"
            return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status
#-----------------------------Administrador-----------------------------------

def get_columns_usuario():
    strsql = 'select * from Usuarios'
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def get_columns_productos():
    strsql = 'select * from Productos'
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def sql_search_user(cedula):
    strsql = 'select * from Usuarios where Cedula = ?', (cedula,)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

def sql_search_product(codigo):
    strsql = 'select * from Productos where Codigo_del_producto = ?', (codigo,)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

def get_clientes():
    strsql = 'select * from Usuarios where rol = ?',('1',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

def get_empleados():
    strsql = 'select * from Usuarios where rol = ?',('2',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

def get_productos():
    strsql = 'select * from Productos'
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

#-------------------------------------LUIS------------------------------
def obtener_info_usuario(id_usuario):
    status = { 'error':None, 'data':None}
    try:
        con=sql_connection()
        cur = con.cursor()
        query=cur.execute("SELECT Cedula, Nombre_y_apellido, Fecha_de_nacimiento,Sexo, Direccion, Ciudad, username FROM Usuarios WHERE id_usuario=?  ",[id_usuario]).fetchone()
        if query!=None:
            status['data']= [query[0],query[1],query[2],query[3],query[4],query[5],query[6]]
            return status
        else:
                
            status['error'] = "Ocurrio un error"
            return status
                      
    except Error:
        status['error'] = "Algo salió mal"
        return status