#--------------------------------------------------------------------
# Importamos el framework Flask
from flask import Flask

# Importamos la función que nos permit el render de los templates,
# recibir datos del form, redireccionar, etc.
from flask import render_template, request,redirect
from flask import send_from_directory, url_for, flash

# Importamos el módulo que permite conectarnos a la BS
from flaskext.mysql import MySQL

# Importamos las funciones relativas a fecha y hora
from datetime import datetime

# Importamos paquetes de interfaz con el sistema operativo.
import os
#--------------------------------------------------------------------


# Creamos la aplicación
app = Flask(__name__)


#--------------------------------------------------------------------
# Creamos la conexión con la base de datos:
mysql = MySQL()
# Creamos la referencia al host, para que se conecte a la base
# de datos MYSQL utilizamos el host localhost
app.config['MYSQL_DATABASE_HOST']='localhost'
# Indicamos el usuario, por defecto es user
app.config['MYSQL_DATABASE_USER']='root'
# Sin contraseña, se puede omitir
app.config['MYSQL_DATABASE_PASSWORD']=''
# Nombre de nuestra BD
app.config['MYSQL_DATABASE_BD']='prueba'
# Creamos la conexión con los datos
mysql.init_app(app)

#DESDE ACA COLOCO TODAS LAS FUNCIONES DE ESTRUCTURA
#--------------------------------------------------------------------
# Proporcionamos la ruta a la raiz del sitio y la pagina inicial
@app.route('/')
def index():
    return render_template('empleados/3_inicial.html')

#--------------------------------------------------------------------
# Función para mostrar el form acerca de, la llama la opcion del pie.
@app.route('/f_acerca')
def f_acerca():
    return render_template('empleados/4_acerca.html')
#--------------------------------------------------------------------
# Función para volver a la pagina principal, la llama la opcion del menu
@app.route('/f_listar')
def f_listar():
#    def index():
    # Creamos una variable que va a contener la consulta sql:
    sql = "SELECT * FROM `prueba`.`cuentas`;"
    # Nos conectamos a la base de datos
    conn = mysql.connect()
    # Sobre el cursor vamos a realizar las operaciones
    cursor = conn.cursor()
    # Ejecutamos la sentencia SQL sobre el cursor
    cursor.execute(sql)
    # Copiamos el contenido del cursor a una variable
    db_empleados = cursor.fetchall()
    # "Commiteamos" (Cerramos la conexión)
    conn.commit()
    # Devolvemos código HTML para ser renderizado
    return render_template('empleados/a_listar.html', empleados = db_empleados)


#--------------------------------------------------------------------
# Función para crear un registro nuevo, la llama la opcion del menu
@app.route('/f_crear')
def f_crear():
    return render_template('empleados/b_crear.html')

#--------------------------------------------------------------------
# Función para mostrar el registro a editar, la llama el boton de listar.html
@app.route('/f_editar/<int:id>')
def f_editar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `prueba`.`cuentas` WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/c_editar.html', empleados=empleados)
#--------------------------------------------------------------------
# Función para mostrar el registro a eliminar, la llama el boton de listar.html
@app.route('/f_mostrar_eliminar/<int:id>')
def f_mostrar_eliminar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `prueba`.`cuentas` WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/d_eliminar.html', empleados=empleados)

#--------------------------------------------------------------------
# Función para eliminar un registro, la llama el boton de confirmación del form eliminar
@app.route('/f_eliminar/<int:id>')
def f_eliminar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `prueba`.`cuentas` WHERE id=%s", (id))
    conn.commit()
    return redirect('/f_listar') # Ejecuto la funcion del programa que lista la base

#--------------------------------------------------------------------

#Función para agregar,(dar de alta) una nueva cuenta.
@app.route('/agregar', methods=['POST'])
def agregar():
    # Recibimos los valores del formulario y los pasamos a variables locales:
    _tipo = request.form['txtTipo']
    _cuenta = request.form['txtCuenta']
    _saldo = request.form['txtSaldo']

    # Nos asegurarnos que todos los datos hayan sido ingresados:
    # OJO NO ANDA ver con programacion comun
    if _tipo == '' or _cuenta == '' or _saldo =='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('b_crear.html'))

     # Y armamos una tupla con esos valores:
    datos = (_tipo, _cuenta, _saldo)

    # Armamos la sentencia SQL que va a almacenar estos datos en la DB:
    sql = "INSERT INTO `prueba`.`cuentas` \
          (`Id`, `Tipo`, `Cuenta`, `Saldo`) \
          VALUES (NULL, %s, %s, %s);"

    conn = mysql.connect()     # Nos conectamos a la base de datos
    cursor = conn.cursor()     # En cursor vamos a realizar las operaciones
    cursor.execute(sql, datos) # Ejecutamos la sentencia SQL en el cursor
    conn.commit()              # Hacemos el commit
    return redirect('/f_listar') # Ejecuto la funcion del programa que lista la base

#--------------------------------------------------------------------

# Función para actualizar los datos de un registro
@app.route('/actualizar', methods=['POST'])
def actualizar():
    # Recibimos los valores del formulario y los pasamos a variables locales:

    _tipo = request.form['txtTipo']
    _cuenta = request.form['txtCuenta']
    _saldo = request.form['numSaldo']
    _id = request.form['txtId']

    # Armamos la sentencia SQL que va a actualizar los datos en la DB:
    sql = "UPDATE `prueba`.`cuentas` SET `Tipo`=%s, `Cuenta`=%s, `Saldo`=%s WHERE Id=%s;"
    # Y la tupa correspondiente
    datos = (_tipo,_cuenta,_saldo,_id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/f_listar') # Ejecuto la funcion del programa que lista la base

#--------------------------------------------------------------------

#--------------------------------------------------------------------
#ESTO FUE LO AGREGADO EN LA RAMA PRUEBA
#--------------------------------------------------------------------

# ACA AGREGO ALGO EN LA RAMA MASTER LOCAL
# ESTO FUE AGREGADO EN LA RAMA MASTER DE GIT


# Estas líneas de código las requiere python para que 
# se pueda empezar a trabajar con la aplicación
if __name__=='__main__':
    #Corremos la aplicación en modo debug
    app.run(debug=True)
#--------------------------------------------------------------------
