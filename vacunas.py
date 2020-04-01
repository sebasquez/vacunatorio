#INTEGRANTES: NATALIA SEPÚLVEDA - NELSON VÁSQUEZ
#INGENIERÍA CIVIL EN INFORMÁTICA UBB 2020

import requests
import json
import times
from flask import Flask, render_template, jsonify, request,flash,url_for
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors
from itertools import cycle

#pip install -r requeriments.txt

app = Flask(__name__)
app.config["MYSQL_DATABASE_USER"] = "root"    #Usuario de la BD
app.config["MYSQL_DATABASE_DB"]  = "vacunatorio" #Nombre de mi base de datos para conectarme
#app.config['MYSQL_DATABASE_PASSWORD'] = 'pass' #clave de usuario de la bd, si no tiene eliminar
app.secret_key = 'python'
app.config['SESSION_TYPE'] = 'filesystem'

mysql = MySQL(app)

mysql.connect_args["autocommit"] = True #Guardar cambios en la BD de forma automatica
mysql.connect_args["cursorclass"] = pymysql.cursors.DictCursor #Transforma las tuplas a diccionarios en los cursores 	


@app.route('/')#Pagina inicio donde estan listados los pacientes
def inicio():
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * FROM paciente") #Muestra los pacientes desde la BD
	paciente=cursor.fetchall()
	return render_template("inicio.html",pacientes=paciente)





@app.route('/paciente/add',methods=["GET","POST"]) #Agregar pacientes desde planilla hacia la BD
def nuevopaciente():
	if request.method=="GET":
		return render_template("nuevopaciente.html")
	if request.method=="POST":
		try:		
			datos=request.form
			rut=datos['RUT']
			validar=validarRut(rut)
			nombre=datos['NOMBRE'].upper()
			fechan=datos['FECHAN_NACIMIENTO']
			if validar==False:
				flash("Error: El Rut ingresado no es correcto")
				return render_template("nuevopaciente.html")
			else:
				cursor_insertar = mysql.get_db().cursor()
				sql="INSERT INTO PACIENTE(RUT,NOMBRE,FECHA_NACIMIENTO) VALUES(%s,%s,%s)"
				cursor_insertar.execute(sql,(rut,nombre,fechan))
				mensaje="Su registró se guardó correctamente"
				return render_template("addDatos.html", e=mensaje)
			
		except Exception as e:
			flash("Error: Este Rut ya tiene un paciente asociado")
			return render_template("nuevopaciente.html")


def validarRut(rut):
	rut = rut.upper();
	rut = rut.replace("-","")
	rut = rut.replace(".","")
	aux = rut[:-1]
	dv = rut[-1:]
	revertido = map(int, reversed(str(aux)))
	factors = cycle(range(2,8))
	s = sum(d * f for d, f in zip(revertido,factors))
	res = (-s)%11
	if str(res) == dv:
		return True
	elif dv=="K" and res==10:
		return True
	else:
		return False




@app.route('/vacunas/add', methods=["POST","GET"])#Agregar nueva vacuna
def nuevavacuna():
	if request.method=="GET":
		return render_template("nuevavacuna.html") #Muestra el formulario a rellenar

	if request.method=="POST": #guardala nueva vacuna en la BD
		try:
			datos=request.form 
			nombre=datos['NOMBRE_ENFERMEDAD'].upper()	
			fecha=times.now()
			cursor_insertar = mysql.get_db().cursor()
			sql="INSERT INTO VACUNA(NOMBRE_ENFERMEDAD,FECHA_CREACION) VALUES(%s,%s)"
			cursor_insertar.execute(sql,(nombre,fecha))
			mensaje="Su registró se guardó correctamente"
			return render_template("addDatos.html", e=mensaje)
			
		except Exception as e:
			flash("Error: Esta vacuna ya existe")
			return render_template("nuevavacuna.html") 
		





@app.route('/addVacuna',methods=['POST']) #Envía el formulario para el paciente seleccionado desde inicio
def addVacuna():
	if request.method=="POST":
		rut=request.form['rut']
		cursor_paciente = mysql.get_db().cursor()
		sql="SELECT * FROM paciente WHERE RUT = %s"
		cursor_paciente.execute(sql,rut)
		paciente=cursor_paciente.fetchall()	

		cursor_vacuna = mysql.get_db().cursor()
		cursor_vacuna.execute("SELECT * FROM vacuna") #Muestra los pacientes desde la BD
		vacuna=cursor_vacuna.fetchall()
		return render_template("addVacuna.html",pacientes=paciente,vacunas=vacuna)
		


@app.route('/addDatosVacuna', methods=['POST']) #Guardar datos vacunación a paciente
def addDatosVacuna():
	if request.method=='POST':
		try:
			datos=request.form
			rut=datos['RUT']
			vacuna=datos['NOMBRE_ENFERMEDAD'].upper()
			fecha=times.now()	
			cursor_insertar = mysql.get_db().cursor()
			sql="INSERT INTO PACIENTE_RECIBE_VACUNA(RUT,NOMBRE_ENFERMEDAD,FECHA_VACUNACION) VALUES(%s,%s,%s)"
			cursor_insertar.execute(sql,(rut,vacuna,fecha))
			mensaje="Su registró se guardó correctamente"
			return render_template("addDatos.html",e = mensaje)

		except Exception as e:
			mensaje2="No fue posible guardar su registro"
			return render_template("addDatos.html",e = mensaje2)

		
	

@app.route('/paciente/vacunas', methods=['GET']) 
def pacientesVacunas():
	if request.method=='GET': #envía los datos para ver las vacunas que ha recibido el paciente
		rut=request.args.get('rut',default=None, type=None)
		cursor= mysql.get_db().cursor()
		sql="SELECT * FROM PACIENTE_RECIBE_VACUNA WHERE RUT = %s"
		cursor.execute(sql,rut)
		vacunas=cursor.fetchall()

		cursor_paciente= mysql.get_db().cursor()
		sql_paciente="SELECT * FROM PACIENTE WHERE RUT = %s"
		cursor_paciente.execute(sql_paciente,rut)
		paciente=cursor_paciente.fetchall()
		return render_template('pacientesVacunas.html',pacientes=paciente,vacunas=vacunas)



@app.route('/vacunas',methods=["GET"])#Listado de las vacunas existentes
def vacunas():
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * FROM vacuna") #Muestra las vacunas desde la BD
	vacunas=cursor.fetchall()
	return render_template("verVacunas.html", vacunas=vacunas)



@app.route('/pacientesPorVacunas',methods=["POST"])#Listado pacientes por vacunas
def pacientesPorVacunas():
	if request.method=="POST":	
		id_vacuna=request.form['NOMBRE_ENFERMEDAD']
		cursor = mysql.get_db().cursor()
		sql="SELECT P.NOMBRE, P.RUT, PV.FECHA_VACUNACION FROM PACIENTE_RECIBE_VACUNA PV, PACIENTE P, VACUNA V " 
		sql+="WHERE PV.RUT=P.RUT "
		sql+="AND PV.NOMBRE_ENFERMEDAD=V.NOMBRE_ENFERMEDAD AND PV.NOMBRE_ENFERMEDAD= %s"
		cursor.execute(sql,id_vacuna) #Muestra las vacunas desde la BD
		vacunados=cursor.fetchall()

		return render_template("pacientesPorVacunas.html", vacunados=vacunados,vacuna=id_vacuna)



if __name__ == "__main__":
	app.run(debug=True)







