import requests
import json
import times
from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors

#pip install -r requeriments.txt
app = Flask(__name__)
app.config["MYSQL_DATABASE_USER"] = "root"    #Usuario de la BD
app.config["MYSQL_DATABASE_DB"]  = "vacunatorio" #Nombre de mi base de datos para conectarme
app.config['MYSQL_DATABASE_PASSWORD'] = '1508' #la clave de mi usuario, en vacunas.sql está mi código de la bd
mysql = MySQL(app)

mysql.connect_args["autocommit"] = True #Guardar cambios en la BD de forma automatica
mysql.connect_args["cursorclass"] = pymysql.cursors.DictCursor #Transforma las tuplas a diccionarios en los cursores 	


@app.route('/')#Pagina inicio donde estan listados los pacientes
def inicio():
	#dejar esta pagina como el menú inicial
	#en la plantilla leo los datos 
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * FROM paciente") #Muestra los pacientes desde la BD
	paciente=cursor.fetchall()
	return render_template("inicio.html",pacientes=paciente)


@app.route('/addVacuna',methods=['POST']) #Listado de vacunas
def addVacuna():
	
	
	#cursor = mysql.get_db().cursor()
	#cursor.execute("SELECT * FROM paciente") #Muestra los pacientes desde la BD
	#paciente=cursor.fetchall()
	rut=request.form['rut']
	cursor_paciente = mysql.get_db().cursor()
	sql="SELECT * FROM paciente WHERE RUT = %s"
	cursor_paciente.execute(sql,rut)
	paciente=cursor_paciente.fetchall()
	
	cursor_vacuna = mysql.get_db().cursor()
	cursor_vacuna.execute("SELECT * FROM vacuna") #Muestra los pacientes desde la BD
	vacuna=cursor_vacuna.fetchall()
	return render_template("addVacuna.html",pacientes=paciente,vacunas=vacuna)
		


@app.route('/addDatosVacuna', methods=['POST']) #Listado de vacunas
def addDatosVacuna():	
	try:
		datos=request.form
		rut=datos['RUT']
		vacuna=datos['NOMBRE_ENFERMEDAD']
		fecha=times.now()	
		cursor_insertar = mysql.get_db().cursor()
		sql="INSERT INTO PACIENTE_RECIBE_VACUNA(RUT,NOMBRE_ENFERMEDAD,FECHA_VACUNACION) VALUES(%s,%s,%s)"
		cursor_insertar.execute(sql,(rut,vacuna,fecha))
		mensaje="Su registró se guardó correctamente"
		return render_template("addDatosVacuna.html",e = mensaje)

		

	except Exception as e:
		mensaje2="No fue posible guardar su registro"
		return render_template("addDatosVacuna.html",e = mensaje2)

	
	





if __name__ == "__main__":
	app.run(debug=True)



