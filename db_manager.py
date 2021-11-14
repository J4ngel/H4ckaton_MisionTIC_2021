import sqlite3
from sqlite3 import Error

import hashlib
from werkzeug.security import check_password_hash

from flask import g
import main

ruta = main.confBd()+"orion.db"
#----->REGISTRO DE UN USUARIO EXTERNO (CLIENTE)
def reg_1(cedula, name, gender, birthday, city, adds, username,phrase, password, rol):
    status={'state':True, 'error':None}
    try:
        with sqlite3.connect("orion.db") as con:
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
        status['error'] = "Algo salió mal" + Error
        return status

#----->REGISTRO DE UN USUARIO INTERNO (EMPLEADO)
def reg_2(cedula, name, job, gender, birthday, city, adds,username, phrase, password, rol):
    status={'state':True, 'error':None}
    try:
        with sqlite3.connect("orion.db") as con:
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
        status['error'] = "Algo salió mal" + Error
        return status

#----->VERIFICACION DE CREDENCIALES      
def login_session(username, password):
    status = {'state':True, 'error':None, 'data':None}
    try:
        with sqlite3.connect("orion.db") as con:
            cur = con.cursor()
            query=cur.execute("SELECT Contrasena, Nombre_y_apellido, rol,id_usuario FROM Usuarios WHERE username=?",[username]).fetchone()
            if query!=None:
                if check_password_hash(query[0],password):
                    status['data']=query
                    return status
                else:
                    status['state'] = False
                    status['error'] = "Credenciales invalidas verifique la cedula y/o la contraseña"
                    return status
                    
            else:
                status['state'] = False
                status['error'] = "Credenciales invalidas verifique la cedula y/o la contraseña"
                return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal "+ Error
        return status

#----->DEVUELVE LA CEDULA SI LAS TRES PREGUNTAS SE RESUELVEN DE FORMA CORRECTA
def recuperar_usuario(name, birthday, phrase):
    status = {'state':True, 'error':None, 'data':None}
    try:
        with sqlite3.connect("orion.db") as con:
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
        status['error'] = "Algo salió mal "+ Error
        return status

#----->ACTUALIZA LA INFORMACIÓN SI SE CUMPLIERON LAS VERIFICACIONES ANTERIORES
def recuperar_pass(password,id_usuario):
    status = {'state':True, 'error':None, 'data':None}
    try:
        with sqlite3.connect("orion.db") as con:
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
        status['error'] = "Algo salió mal "+ Error
        return status

#------>ELIMINAR CUENTAS POR id_usuario
def eliminar_cuenta(id_usuario):
    status = {'state':True, 'error':None, 'data':None}
    try:
        with sqlite3.connect(ruta) as con:
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
        status['error'] = "Algo salió mal "+ Error
        return status
#-----------------------------Administrador-----------------------------------
def sql_connection():
    try:
        if 'con' not in g:
            path = main.confBd()
            g.con = sqlite3.connect(path + "orion.db")
        return g.con
    except Error:
        print(Error)

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
        with sqlite3.connect("orion.db") as con:
            cur = con.cursor()
            query=cur.execute("SELECT Cedula, Nombre_y_apellido, Fecha_de_nacimiento,Sexo, Direccion, Ciudad FROM Usuarios WHERE id_usuario=?  ",[id_usuario]).fetchone()
            if query!=None:
                status['data']= [query[0],query[1],query[2],query[3],query[4],query[5]]
                return status
            else:
                    
                status['error'] = "Ocurrio un error"
                return status
                      
    except Error:
        status['error'] = "Algo salió mal "+ Error
        return status

#--------------------------------Yessid------------------
def lista_productos():
    status = { 'error':None, 'data':None}
    try:
        with sqlite3.connect(ruta) as con:
            cur = con.cursor()
            query1=cur.execute("SELECT * FROM Productos").fetchall()
            if query1!=None:
                status['data']= query1 #status['data']=[[]]
                print(status['data'])
                return status['data']
            else:
                    
                status['error'] = "Ocurrio un error"
                return status
                      
    except Error:
        status['error'] = "Algo salió mal "+ Error
        return status

def consulta_produc(id):
    status = {'error':None, 'data':None}
    try:
        with sqlite3.connect(ruta) as con:
            cur = con.cursor()
            query1=cur.execute("SELECT * FROM Productos WHERE Codigo_del_producto=?",[id]).fetchone()
            if query1!=None:
                status['data']= query1 #status['data']=[[]]
                print(status['data'])
                return status['data']
            else:                    
                status['error'] = "Ocurrio un error"
                return status
                      
    except Error:
        status['error'] = "Algo salió mal "+ Error
        return status

def actualizar_produc(id,nombre,precio,procentaje,categoria,bono):
    try:
        with sqlite3.connect(ruta) as con:
            cur = con.cursor()
            query1=cur.execute("UPDATE Productos SET Nombre_del_producto =?,Precio_unitario =?,Porcentaje_de_promocion =?,Categoria_del_producto =?,Bono =? WHERE Codigo_del_producto =?",[nombre,precio,procentaje,categoria,bono,id])
            con.commit()
            print("actualizo")          
    except Error:
        return "Error"

#Luis --> Eliminar Producto
def eliminar_producto(id):
    try:
        with sqlite3.connect(ruta) as con:
            cur = con.cursor()
            query1=cur.execute("DELETE FROM Productos WHERE Codigo_del_producto = ?",[id])
            con.commit()
                 
    except Error:
        return "Error"

#----->Yessid / Jackie (Registro de un producto nuevo)
def nuevo_producto(codigo, nombre, tipo, cantidad, unidad, precio, descuento, bono, acumulado):
    status={'state':True, 'error':None}
    
    try:
        con=sql_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO Productos(Codigo_del_producto, Nombre_del_producto, Tipo_producto, Cantidad_de_unidades_actuales_totales_en_el_inventario, Tipo_de_unidad, Precio_unitario, Porcentaje_de_promocion, Bono, Acumulados_descontados) VALUES (?,?,?,?,?,?,?,?,?)",(codigo, nombre, tipo, cantidad, unidad, precio, descuento, bono, acumulado,))
        con.commit()
            
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal"
        return status
